import os
from flask import Flask, render_template, request, jsonify, abort
from services.database import init_db, save_check, get_recent_checks, save_feedback
from services.domain_check import check_domains
from services.predictor import predict, load_model
from config import MAX_INPUT_LENGTH

app = Flask(__name__)

# Initialize database on startup
init_db()

@app.route("/", methods=["GET"])
def index():
    """Render index page with submission form and recent check history."""
    try:
        recent_checks = get_recent_checks(limit=10)
    except Exception as e:
        recent_checks = []
        # In a real app, log the exception. Here we keep it quiet.
        
    return render_template("index.html", recent_checks=recent_checks, error=None, result=None)

@app.route("/check", methods=["POST"])
def check():
    """Validate input text, call prediction and domain checking, store result, and render."""
    text = request.form.get("text", "")
    trimmed_text = text.strip()
    
    # Validation
    if not trimmed_text:
        recent_checks = get_recent_checks(limit=10)
        return render_template("index.html", recent_checks=recent_checks, error="Please enter some text to check.", result=None)
        
    if len(trimmed_text) > MAX_INPUT_LENGTH:
        recent_checks = get_recent_checks(limit=10)
        return render_template(
            "index.html", 
            recent_checks=recent_checks, 
            error=f"Text exceeds the limit of {MAX_INPUT_LENGTH} characters.", 
            result=None
        )
        
    try:
        # Call domain check
        domain_result = check_domains(trimmed_text)
        
        # Call predictor
        prediction = predict(trimmed_text)
        
        # Merge result
        payload = {
            "submitted_text": trimmed_text,
            "predicted_label": prediction["label"],
            "confidence": prediction["confidence"],
            "influential_terms": prediction["influential_terms"],
            "detected_domain": domain_result["detected_domain"],
            "domain_status": domain_result["domain_status"]
        }
        
        # Save check to database
        check_id = save_check(payload)
        payload["id"] = check_id
        
        recent_checks = get_recent_checks(limit=10)
        return render_template("index.html", recent_checks=recent_checks, error=None, result=payload)
        
    except FileNotFoundError as e:
        # Graceful handling for model not trained yet
        recent_checks = get_recent_checks(limit=10)
        error_msg = "The classification model has not been trained yet. Please run `python scripts/train_model.py` first."
        return render_template("index.html", recent_checks=recent_checks, error=error_msg, result=None)
        
    except Exception as e:
        recent_checks = get_recent_checks(limit=10)
        return render_template("index.html", recent_checks=recent_checks, error="An unexpected error occurred during prediction.", result=None)

@app.route("/feedback/<int:check_id>", methods=["POST"])
def feedback(check_id):
    """Receive upvote/downvote feedback and save to database."""
    vote = request.form.get("vote") or request.json.get("vote")
    if not vote or vote not in ("upvote", "downvote"):
        return jsonify({"error": "Invalid vote value. Must be 'upvote' or 'downvote'."}), 400
        
    try:
        save_feedback(check_id, vote)
        return jsonify({"status": "success", "message": "Feedback recorded."})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to save feedback."}), 500

@app.route("/health", methods=["GET"])
def health():
    """System health check endpoint."""
    health_status = {
        "status": "healthy",
        "database": "available",
        "model": "loaded"
    }
    
    # Check database connectivity
    try:
        get_recent_checks(limit=1)
    except Exception:
        health_status["database"] = "unavailable"
        health_status["status"] = "unhealthy"
        
    # Check model loading status
    try:
        load_model()
    except Exception:
        health_status["model"] = "not_loaded_or_unavailable"
        # We don't mark the whole app unhealthy if the model isn't trained yet, but keep status reporting
        
    return jsonify(health_status)

if __name__ == "__main__":
    app.run(debug=True)
