
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
                '''
            }
        }

        stage('Automated Tests') {
            steps {
                sh '.venv/bin/pytest -v'
            }
        }

        stage('Code Security Scan') {
            steps {
                sh '.venv/bin/bandit -r app.py'
            }
        }

        stage('Dependency Audit') {
            steps {
                sh '.venv/bin/pip-audit -r requirements.txt'
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
            echo 'QRForge CI/CD pipeline finished.'
        }

        success {
            echo 'Build, tests, security checks and deployment succeeded.'
        }

        failure {
            echo 'Pipeline failed. Check the stage console output.'
        }
    }
}
