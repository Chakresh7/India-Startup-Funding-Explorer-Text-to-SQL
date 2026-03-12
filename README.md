# 🚀 India Startup Funding Explorer

A Text-to-SQL app that lets you query Indian startup funding data using plain English — no SQL knowledge needed.

## 🔥 Live Demo
[Try it here →](https://your-app.streamlit.app)

## 💡 What it does
- Type a question in plain English
- Groq (LLaMA 3.3) converts it to SQL
- SQLite runs the query
- Results display instantly

## 🛠 Tech Stack
- **LLM**: Groq API (LLaMA 3.3 70B)
- **Framework**: LangChain
- **UI**: Streamlit
- **Database**: SQLite

## 📊 Dataset
40+ funding rounds from Indian startups including Zepto, CRED, Razorpay, Meesho, PhonePe, Swiggy, and more — across Fintech, Edtech, EV, Healthtech, and E-Commerce sectors.

## 🚀 Run locally

```bash
git clone https://github.com/yourusername/india-startup-funding-explorer
cd india-startup-funding-explorer
pip install -r requirements.txt
python create_db.py
streamlit run app.py
```

Add your Groq API key in `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_key_here"
```

## 📌 Example queries
- "Which startups raised more than $300M?"
- "Top 5 startups by valuation"
- "Which city has the most funded startups?"
- "Average funding amount by sector"
- "Show all Fintech startups that raised in 2023"

## 👨‍💻 Built by
[Chakresh](https://linkedin.com/in/yourprofile) — AI/ML Student & Builder
