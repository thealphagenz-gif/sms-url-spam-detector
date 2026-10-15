import os
from flask import Flask, render_template, request, jsonify
from detector import SpamDetector, analyze_url
app = Flask(__name__)
detector = SpamDetector()

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/sms")
def sms():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Please enter an SMS message first."}), 400
    return jsonify(detector.predict_sms(message))

@app.post("/api/url")
def url():
    data = request.get_json(silent=True) or {}
    value = str(data.get("url", "")).strip()
    if not value:
        return jsonify({"error": "Please enter a URL first."}), 400
    return jsonify(analyze_url(value))

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0").strip().lower() in {"1", "true", "yes"}
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=debug)
