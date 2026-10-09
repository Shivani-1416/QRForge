
from flask import Flask, request, send_file, render_template_string
import qrcode
from io import BytesIO

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>QRForge</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 80px auto;
            max-width: 600px;
            background: #f4f6f8;
        }
        input, button { padding: 12px; margin: 8px; }
        input { width: 70%; }
        button {
            background: #2563eb;
            color: white;
            border: none;
            cursor: pointer;
        }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>QRForge</h1>
    <p>Generate a QR code from text or a URL.</p>

    <form method="POST">
        <input name="text" maxlength="500"
               placeholder="Enter text or URL" required>
        <button type="submit">Generate QR</button>
    </form>

    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}

    {% if text %}
        <p>Your QR code is ready!</p>
        <img src="/qr-image?text={{ text|urlencode }}"
             alt="Generated QR code">
        <p>
            <a href="/qr-image?text={{ text|urlencode }}&download=1">
                Download QR Code
            </a>
        </p>
    {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    text = ""
    error = None

    if request.method == "POST":
        text = request.form.get("text", "").strip()

        if not text:
            error = "Please enter some text or a URL."
        elif len(text) > 500:
            error = "Input must be 500 characters or fewer."
            text = ""

    return render_template_string(HTML, text=text, error=error)


@app.route("/qr-image")
def qr_image():
    text = request.args.get("text", "")

    if not text or len(text) > 500:
        return "Invalid QR input", 400

    image = qrcode.make(text)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/png",
        as_attachment=request.args.get("download") == "1",
        download_name="qrforge.png"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
