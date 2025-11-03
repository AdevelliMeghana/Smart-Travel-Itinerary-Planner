from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API key from environment variable
genai.configure(api_key="Your_api_key")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def generate_itinerary():
    try:
        destination = request.form.get("destination", "").strip()
        days = request.form.get("days", "").strip()
        interests = request.form.get("interests", "").strip()

        prompt = f"""
        Create a detailed {days}-day travel itinerary for {destination}.
        Include:
        - Day-wise plans
        - Must-visit attractions
        - Local food suggestions
        - Hidden gems
        - Approximate budget per day and total budget
        Focus on these interests: {interests}.
        Present it clearly.
        """

        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        response = model.generate_content(prompt)
        itinerary = response.text.strip() if response.text else "No response generated."
        return jsonify({"itinerary": itinerary})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(debug=True)
