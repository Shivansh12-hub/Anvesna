from flask import Flask, request, jsonify
from genai import modelPred, health_risk, pregnancyHealthChat
import numpy as np
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/AI_Report", methods=["POST"])
def report():
    data = request.get_json(force=True)  # Get JSON from Postman
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    sample_data = data.get("sample_data")
    sample_risk = data.get("sample_risk")

    if sample_data is None or sample_risk is None:
        return jsonify({"error": "sample_data and sample_risk are required"}), 400

    # Process input data
    sample_data_processed = modelPred(sample_data)
    risk_status_processed = health_risk(sample_risk=sample_risk)

    # Convert any NumPy arrays to lists for JSON serialization
    if isinstance(sample_data_processed, np.ndarray):
        sample_data_processed = sample_data_processed.tolist()
    if isinstance(risk_status_processed, np.ndarray):
        risk_status_processed = risk_status_processed.tolist()

    # Generate pregnancy health report
    user_question = "Generate concise pregnancy health report in JSON format"
    answer_raw = pregnancyHealthChat(sample_data_processed, risk_status_processed, user_question)

    # Convert model answer from string to dict if possible
    try:
        answer_json = json.loads(answer_raw)
    except:
        answer_json = {"report": answer_raw}

    return jsonify({
        "sample_data": sample_data_processed,
        "sample_risk": sample_risk,
        "risk_status": risk_status_processed,
        "AI_report": answer_json
    })


if __name__ == '__main__':
    app.run(debug=True)
