from flask import Flask, request, jsonify
from utils.checker import check_card

app = Flask(__name__)

@app.route("/")
def index():
    return "Credit Card Checker API - Atmos Energy Gateway"

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    if not data or "cc" not in data:
        return jsonify({"error": "Missing 'cc' field (format: 4111111111111111|12|25|123)"}), 400
    
    result = check_card(data["cc"])
    return jsonify(result)

if __name__ == "__main__":
    app.run()
