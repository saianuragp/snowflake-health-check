# 📦 Snowflake Storage Monitor with Streamlit + Cortex AI

Monitor your Snowflake storage usage like a pro. This interactive app uses **Streamlit** and **Snowflake Cortex AI** to visualize, detect, and summarize storage growth across tables, databases, and schemas.

---

## 🚀 Features

- 📈 **Top Growing Tables**: View historical trends over the past N days
- ⚠️ **Anomaly Detection**: Identify unusual spikes using Cortex AI
- 🔮 **Forecasting**: Predict storage usage for the next 7 days
- 🧠 **AI Summaries**: Get natural language insights powered by GPT (Cortex)
- 🔔 **Slack/Teams Alerts** (Optional)

---

## 🛠️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/snowflake-ai-monitor.git
cd snowflake-ai-monitor
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file or export these:
```env
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account.region.gcp
SNOWFLAKE_WAREHOUSE=your_wh
```

### 4. Run the App
```bash
streamlit run app.py
```

---

## 💬 Cortex AI Usage
This project uses the following Cortex AI models:
- `ML.ANOMALY_DETECTION` for identifying outliers
- `ML.FORECAST` for predicting trends
- `CORTEX.COMPLETE` (GPT) for AI-powered summaries

> All AI is run natively in Snowflake — no data leaves your environment.

---

## 🖼️ Dashboard Preview

| Table       | Date    | Size (GB) | Anomaly |
|-------------|---------|-----------|---------|
| SALES       | 04-25   | 9.61      | ✅ Yes   |
| LOGS        | 04-19   | 6.47      | ✅ Yes   |
| EVENTS      | 04-27   | 2.19      | ✅ Yes   |

---

## 📬 Contact / Custom Builds
Looking to:
- Add Slack/Teams alerts?
- Schedule monitoring via Snowflake Tasks?
- Deploy this at scale for your org?

📩 [Your LinkedIn or Contact Form](https://linkedin.com/in/yourprofile)

---

## 🔗 Try It Live / Fork It
**👉 [github.com/your-username/snowflake-ai-monitor](https://github.com/your-username/snowflake-ai-monitor)**

---

## 📚 Related Tags
#Snowflake #Streamlit #CortexAI #Monitoring #LLMops #DataEngineering #FinOps #AI
