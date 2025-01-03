import qrcode
from flask import Flask, request, render_template_string, send_file
import os

app = Flask(__name__)

# Function to load the click count from a file
def load_click_count(file_path="click_count.txt"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

# Function to save the click count to a file
def save_click_count(count, file_path="click_count.txt"):
    with open(file_path, "w") as f:
        f.write(str(count))

# Global click counter
click_count = load_click_count()

# QR Code generator function
def generate_qr_code(link, file_name="/tmp/qrcode.png"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)

@app.route("/", methods=["GET", "POST"])
def index():
    global click_count
    if request.method == "POST":
        link = request.form.get("link")
        if link:
            click_count += 1  # Increment the click counter
            save_click_count(click_count)  # Save the updated count
            generate_qr_code(link)
            return send_file("/tmp/qrcode.png", as_attachment=True)

    # HTML with dynamic counter display
    return render_template_string('''
    <!doctype html>
    <html>
        <head>
            <title>QR Code Generator</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #6DD5FA, #FF758C);
                    color: #333;
                    text-align: center;
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }
                .counter {
                    position: absolute;
                    top: 20px;
                    right: 20px;
                    background: #fff;
                    color: #333;
                    padding: 10px 20px;
                    border-radius: 5px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
                    font-size: 1.1rem;
                    font-weight: bold;
                }
                h1 {
                    font-size: 3rem;
                    margin-bottom: 20px;
                    color: #fff;
                    text-shadow: 2px 2px 4px #333;
                }
                form {
                    background: #fff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    max-width: 400px;
                    width: 100%;
                }
                label {
                    font-size: 1.2rem;
                    margin-bottom: 10px;
                    display: block;
                    color: #333;
                }
                input[type="text"] {
                    width: 100%;
                    padding: 10px;
                    font-size: 1rem;
                    margin-bottom: 15px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
                button {
                    background-color: #6DD5FA;
                    color: #fff;
                    border: none;
                    padding: 10px 20px;
                    font-size: 1.2rem;
                    cursor: pointer;
                    border-radius: 5px;
                    transition: background 0.3s;
                }
                button:hover {
                    background-color: #FF758C;
                }
            </style>
        </head>
        <body>
            <div class="counter">QR Code Generated: {{ click_count }} times</div>
            <h1>QR Code Generator</h1>
            <form method="POST">
                <label for="link">Paste the link here:</label>
                <input type="text" id="link" name="link" placeholder="Enter website link" required>
                <button type="submit">Generate QR Code</button>
            </form>
        </body>
    </html>
    ''', click_count=click_count)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
