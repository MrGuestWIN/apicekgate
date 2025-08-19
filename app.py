from flask import Flask, request, jsonify, render_template_string
from utils.checker import check_card

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Welcome to MrGuest API</title>
        <style>
            body { font-family: sans-serif; text-align: center; padding: 50px; background: #111; color: #eee; }
            h1 { color: #33ff99; }
            .box { background: #222; padding: 20px; border-radius: 10px; display: inline-block; }
            a { color: #33ff99; text-decoration: none; border: 1px solid #33ff99; padding: 5px 10px; border-radius: 5px; }
            a:hover { background: #33ff99; color: #000; }
        </style>
    </head>
    <body>
        <div class="box">
            <h1>­ЪДа MrGuest API Gateway</h1>
            <p>Use this API to check fullz & credit card details.</p>
            <a href="https://github.com/MrGuestWIN">View Source</a>
        </div>
    </body>
    </html>
    """)

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    if not data or "cc" not in data:
        return jsonify({"error": "Missing 'cc' field (format: fullz)"}), 400

    result = check_card(data["cc"])
    return jsonify(result)

if __name__ == "__main__":
    app.run()
