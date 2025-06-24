import os
import sqlite3
import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# 🔹 Utility: Database connection
def get_db_connection():
    conn = sqlite3.connect("med_tracker.db")
    conn.row_factory = sqlite3.Row
    return conn

# 🔹 Route: Home
@app.route("/")
def home():
    return render_template("home.html")

# 🔹 Route: Medication Planner
@app.route("/planner", methods=["GET", "POST"])
def planner():
    with get_db_connection() as conn:
        if request.method == "POST":
            drug = request.form.get("drug")
            time = request.form.get("time")
            frequency = request.form.get("frequency")

            if drug and time and frequency:
                conn.execute(
                    "INSERT INTO medications (drug, dose_time, frequency) VALUES (?, ?, ?)",
                    (drug, time, frequency)
                )
                conn.commit()

        meds = conn.execute("SELECT * FROM medications ORDER BY created_at DESC").fetchall()
    return render_template("planner.html", medications=meds)

# 🔹 Route: Log Dose
@app.route("/log_dose/<int:med_id>", methods=["POST"])
def log_dose(med_id):
    with get_db_connection() as conn:
        conn.execute("INSERT INTO dose_logs (med_id) VALUES (?)", (med_id,))
        conn.commit()
    return redirect("/planner")

# 🔹 Route: Dashboard (Summary + History)
@app.route("/dashboard")
def dashboard():
    with get_db_connection() as conn:
        meds = conn.execute("""
            SELECT m.id, m.drug, m.dose_time, m.frequency,
                   COUNT(d.id) AS taken_count
            FROM medications m
            LEFT JOIN dose_logs d ON m.id = d.med_id
            GROUP BY m.id
        """).fetchall()

        med_logs = []
        for med in meds:
            logs = conn.execute("""
                SELECT taken_at FROM dose_logs
                WHERE med_id = ?
                ORDER BY taken_at DESC
            """, (med["id"],)).fetchall()

            med_logs.append({
                "id": med["id"],
                "drug": med["drug"],
                "dose_time": med["dose_time"],
                "frequency": med["frequency"],
                "taken_count": med["taken_count"],
                "logs": [log["taken_at"] for log in logs]
            })

    return render_template("dashboard.html", med_logs=med_logs)

# 🔹 Route: Drug-Food Interaction Checker
@app.route("/check", methods=["POST"])
def check_interaction():
    drug = request.form.get("drug", "").strip().lower()
    food = request.form.get("food", "").strip().lower()

    if not drug or not food:
        return """
        <h2>⚠️ Please enter both drug and food.</h2>
        <a href='/' style='color:#007bff;'>🔙 Go Back</a>
        """

    # Aliases and advice
    food_aliases = {
        "spinach": "vitamin K", "grapefruit": "grapefruit",
        "milk": "calcium", "banana": "potassium", "cheese": "tyramine"
    }

    friendly_tips = {
        "vitamin K": "Vitamin K (e.g., in spinach) may reduce blood thinner effectiveness.",
        "grapefruit": "Grapefruit may interfere with liver enzymes, increasing side effects.",
        "calcium": "Calcium may reduce absorption of some antibiotics or thyroid meds.",
        "potassium": "Excess potassium may harm those on heart or kidney meds.",
        "tyramine": "Tyramine (e.g., in aged cheese) can spike BP with some antidepressants."
    }

    search_terms = [food]
    substance = food_aliases.get(food)
    if substance:
        search_terms.append(substance)

    try:
        url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug}"
        response = requests.get(url)
        data = response.json()

        interaction_info = ""
        if "results" in data:
            sections = ["food_interactions", "warnings", "precautions", "drug_interactions"]
            for section in sections:
                texts = data["results"][0].get(section, [])
                for text in texts:
                    for term in search_terms:
                        if term.lower() in text.lower():
                            highlighted = text.replace(term, f"<b style='color:#d9534f'>{term}</b>")
                            interaction_info += f"<p><strong>{section.replace('_',' ').title()}:</strong><br>{highlighted}</p><hr>"

        if interaction_info:
            return f"""
                <h2>⚠️ Interaction Detected: <span style='color:#dc3545'>{drug.title()}</span> + <span style='color:#dc3545'>{food.title()}</span></h2>
                <p>Based on FDA data, consuming <b>{food}</b> while using <b>{drug.title()}</b> may pose health risks or reduce effectiveness.</p>
                <div style='background:#fff3cd;padding:15px;border-left:5px solid #ffc107;margin-top:20px;'>{interaction_info}</div>
                {f"<div style='background:#e2f0d9;padding:12px;border-left:5px solid #28a745;margin-top:10px;'><b>💡 Tip:</b> " + friendly_tips.get(substance, "") + "</div>" if substance in friendly_tips else ""}
                <a href='/' style='display:inline-block;margin-top:20px;color:#007bff;'>🔙 Check Another</a>
            """
        else:
            return f"""
                <h2>✅ No known interaction found between <b>{drug.title()}</b> and <b>{food.title()}</b>.</h2>
                <a href='/' style='color:#007bff;'>🔙 Try Again</a>
            """
    except Exception as e:
        return f"""
            <h2>❌ Error occurred:</h2>
            <div style='color:#d9534f;background:#f8d7da;padding:10px;border-left:4px solid #dc3545;'>{str(e)}</div>
            <a href='/' style='color:#007bff;'>🔙 Go Back</a>
        """

# 🔹 Route: Explainable AI for interaction
@app.route("/explain/<drug>/<food>")
def explain(drug, food):
    # Build file path
    file_path = f"static/fda_data/{drug.lower()}_{food.lower()}.txt"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            fda_data = f.read()
    else:
        fda_data = "❌ No FDA warning found for this combination."

    summary = f"Consuming {food} while on {drug} may interfere with effectiveness or safety."
    mechanism = f"{food} may interact with how {drug} is metabolized — possibly through nutrients like Vitamin K or enzymes."
    tip = f"Always consult your doctor and keep your {food} intake consistent while on {drug}."

    return render_template("explainable_ai_result.html",
                           drug=drug.title(), food=food.title(),
                           summary=summary, mechanism=mechanism, tip=tip,
                           fda_warning=fda_data)

# 🔁 Entry point
if __name__ == "__main__":
    app.run(debug=True)
