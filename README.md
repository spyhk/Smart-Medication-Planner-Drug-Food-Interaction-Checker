# 💊 Drug & Food Interaction Advisor + Smart Medication Planner

An intelligent Flask web app to help users track medications, set dosage reminders, and check for **drug-food interactions** using FDA data — now with a clean UI, local database support, and explainable AI features.

---

## 🚀 Features

✅ **Drug-Food Interaction Checker**  
✅ **Medication Reminder Planner (LocalStorage + SQLite)**  
✅ **Voice Input for Drug & Food**  
✅ **Explainable AI Summary Page**  
✅ **Clean & Responsive UI with Dashboard Template**  
🛠️ **FDA API Integration (Live Lookup)**

---

## 🗂️ Project Structure

DRUG_FOOD_ADVISOR/
│
├── templates/
│ ├── home.html # Drug-Food Input UI
│ ├── planner.html # Medication planner UI
│ ├── explainable_ai_result.html # Explainable AI result view
│ ├── dashboard.html # Placeholder for AI Trends
│
├── app.py # Main Flask App
├── init_db.py # SQLite DB initializer
├── add_sample_data.py # Optional sample data filler
├── med_tracker.db # Local SQLite database
├── static.css # Optional styling file


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/drug-food-advisor.git
cd drug-food-advisor

2️⃣ Install Python Requirements
bash
Copy code
pip install flask requests
3️⃣ Initialize the SQLite Database
bash
Copy code
python init_db.py
Creates med_tracker.db with table: medications

4️⃣ Run the Application
bash
Copy code
python app.py
Access the app in your browser at http://127.0.0.1:5000

📸 Screenshots
🔍 Drug & Food Interaction Checker

📋 Medication Planner

💡 Explainable AI Output

📦 Features in Progress
📊 Dashboard Analytics with Charts

🔔 Dose Notifications

🔐 User Login System

🌐 Cloud Sync or Google Drive Backup

🤖 LLM Integration for Natural Explanation

📱 Mobile-first PWA or App Version

🤖 Explainable AI
The project uses simple rule-based explanations for interactions based on FDA descriptions and keywords (e.g., Vitamin K interference). We plan to extend this to:

Highlight causes using keyword colors

Summarize interaction severity

Possibly integrate LLM (like ChatGPT) for custom explanation

🛡 Disclaimer
This application is for informational purposes only and not a substitute for professional medical advice. Always consult your healthcare provider.

🧑‍💻 Author
  Developed by [SPYHK]
B.Tech (AI & DS) | Final Year Project | 2025

📝 License
MIT License – Use it freely, but cite the original work if modified.

yaml
Copy code

---

### 📥 Want This as a File?

Let me know and I can export this `README.md` as:

- Plain `.md` file for GitHub
- `.pdf` version
- `.docx` documentation

Would you like it exported now?
