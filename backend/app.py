"""PocketSmart AI - Flask backend. Serves the API and the frontend."""
import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from backend import ai_service as ai

FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
app = Flask(__name__, static_folder=str(FRONTEND), static_url_path="")
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB uploads
ALLOWED_IMAGES = {"image/jpeg", "image/png", "image/webp"}


def error(message, code=400):
    return jsonify({"error": message}), code


def parse_budget(value):
    try:
        budget = float(value)
    except (TypeError, ValueError):
        raise ValueError("Enter a valid budget in rupees.")
    if budget < 500:
        raise ValueError("Budget must be at least ₹500.")
    return budget


def run(builder):
    try:
        return jsonify(builder())
    except ValueError as e:
        return error(str(e), 400)
    except RuntimeError as e:
        return error(str(e), 500)
    except Exception as e:  # Gemini/network errors
        app.logger.exception("AI call failed")
        return error(f"AI request failed: {e}", 502)


@app.get("/")
def index():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "model": ai.MODEL})


@app.post("/api/home")
def home():
    def build():
        d = request.get_json(silent=True) or {}
        budget = parse_budget(d.get("budget"))
        items = [
            {"room": str(i.get("room", "Room")), "item": str(i.get("item", "")),
             "qty": max(1, int(i.get("qty", 1)))}
            for i in d.get("items", []) if i.get("item")
        ]
        if not items:
            raise ValueError("Add at least one item to plan.")
        return ai.generate_plan(ai.home_prompt(budget, items), budget)
    return run(build)


@app.post("/api/party")
def party():
    def build():
        d = request.get_json(silent=True) or {}
        budget = parse_budget(d.get("budget"))
        guests = int(d.get("guests") or 0)
        if guests < 1:
            raise ValueError("Enter the number of guests.")
        prompt = ai.party_prompt(budget, guests, d.get("event", "birthday"),
                                 d.get("venue", "home"), d.get("city", ""))
        return ai.generate_plan(prompt, budget)
    return run(build)


@app.post("/api/jewelry")
def jewelry():
    def build():
        budget = parse_budget(request.form.get("budget"))
        image = None
        file = request.files.get("outfit")
        if file and file.filename:
            if file.mimetype not in ALLOWED_IMAGES:
                raise ValueError("Upload a JPG, PNG or WEBP image.")
            image = (file.read(), file.mimetype)
        prompt = ai.jewelry_prompt(budget, request.form.get("occasion", "wedding"),
                                   request.form.get("style", "traditional"),
                                   request.form.get("notes", ""), image is not None)
        return ai.generate_plan(prompt, budget, image)
    return run(build)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", 5000)), debug=True)
