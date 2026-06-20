"""
MedSafe AI - Medicine Interaction Checker
Flask + OpenAI Powered Healthcare Application
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
import json
from datetime import datetime
from utils.ai_engine import check_interactions, chat_followup
from utils.helpers import format_timestamp, validate_medicines

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "medsafe-hackathon-2024")
CORS(app)


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Main page"""
    return render_template("index.html")


@app.route("/api/check", methods=["POST"])
def check():
    """
    POST /api/check
    Body: { "medicines": ["Warfarin", "Aspirin", ...] }
    Returns AI-generated interaction analysis
    """
    data = request.get_json()
    medicines = data.get("medicines", [])

    # Validate input
    valid, error = validate_medicines(medicines)
    if not valid:
        return jsonify({"error": error}), 400

    # Store in session for follow-up context
    session["medicines"] = medicines
    session["chat_history"] = []

    # Get AI analysis
    result = check_interactions(medicines)

    if result["success"]:
        # Save to session history
        session["chat_history"] = [
            {"role": "user", "content": result["user_prompt"]},
            {"role": "assistant", "content": result["analysis"]}
        ]
        return jsonify({
            "success": True,
            "analysis": result["analysis"],
            "medicines": medicines,
            "timestamp": format_timestamp(),
            "severity_summary": result.get("severity_summary", "unknown")
        })
    else:
        return jsonify({"error": result["error"]}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    POST /api/chat
    Body: { "message": "What should I do if I feel dizzy?" }
    Returns follow-up AI response with context
    """
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    history = session.get("chat_history", [])
    medicines = session.get("medicines", [])

    result = chat_followup(user_message, history, medicines)

    if result["success"]:
        # Update session history
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": result["response"]})
        session["chat_history"] = history

        return jsonify({
            "success": True,
            "response": result["response"],
            "timestamp": format_timestamp()
        })
    else:
        return jsonify({"error": result["error"]}), 500


@app.route("/api/report", methods=["POST"])
def report():
    """
    POST /api/report
    Returns a structured JSON report for download
    """
    data = request.get_json()
    medicines = data.get("medicines", [])
    analysis = data.get("analysis", "")

    report_data = {
        "report_id": f"MEDSAFE-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "generated_at": format_timestamp(),
        "medicines_checked": medicines,
        "medicine_count": len(medicines),
        "analysis": analysis,
        "disclaimer": "This report is for informational purposes only. Always consult a licensed healthcare provider before making any medication decisions."
    }
    return jsonify(report_data)


@app.route("/api/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "MedSafe AI", "version": "1.0.0"})


# ─── Error Handlers ────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# ─── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    print(f"\n🏥 MedSafe AI running at http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
