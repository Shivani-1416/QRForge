pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                    .venv/bin/pip install pytest bandit pip-audit
                    mkdir -p reports
                '''
            }
        }

        stage('Automated Tests') {
            steps {
                sh '''
                    .venv/bin/pytest -v \
                        --junitxml=reports/pytest-report.xml
                '''
            }
        }

        stage('Code Security Scan') {
            steps {
                sh '''
                    .venv/bin/bandit -r app.py \
                        -f json \
                        -o reports/bandit-report.json
                '''
            }
        }

        stage('Dependency Audit') {
            steps {
                sh '''
                    .venv/bin/pip-audit -r requirements.txt \
                        --format json \
                        --output reports/dependency-audit.json
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t qrforge:latest .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f qrforge-app || true
                    docker run -d \
                        --name qrforge-app \
                        --restart unless-stopped \
                        -p 5000:5000 \
                        qrforge:latest
                '''
            }
        }
    }

    post {
        always {
            script {
                def result = currentBuild.currentResult ?: 'UNKNOWN'

                sh """
                    mkdir -p reports
                    cat > reports/pipeline-summary.txt <<'EOF'
                    QRForge CI/CD Pipeline Report
                    Build Number: ${env.BUILD_NUMBER}
                    Build URL: ${env.BUILD_URL}
                    Final Status: ${result}
                    EOF
                """

                archiveArtifacts artifacts: 'reports/*',
                                 allowEmptyArchive: true

                junit testResults: 'reports/pytest-report.xml',
                      allowEmptyResults: true

                echo 'QRForge CI/CD pipeline finished.'
            }
        }

        success {
            echo 'Build, tests, security checks and deployment succeeded.'
        }

        failure {
            echo 'Pipeline failed. Check the stage console output and archived reports.'
        }
    }
}