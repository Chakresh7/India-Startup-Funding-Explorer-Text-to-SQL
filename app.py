import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

st.set_page_config(
    page_title="India Startup Funding Explorer",
    page_icon="🚀",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #888;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    .example-chip {
        display: inline-block;
        background: #f4f4f4;
        border: 1px solid #e0e0e0;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 0.82rem;
        margin: 4px 4px 4px 0;
        cursor: pointer;
        color: #333;
    }

    .sql-box {
        background: #0f0f0f;
        color: #a8ff78;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        font-family: 'Courier New', monospace;
        font-size: 0.88rem;
        margin: 0.5rem 0 1rem 0;
        border-left: 3px solid #a8ff78;
    }

    .stat-card {
        background: #fafafa;
        border: 1px solid #ebebeb;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
    }

    .stat-number {
        font-family: 'Syne', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #111;
    }

    .stat-label {
        font-size: 0.78rem;
        color: #888;
        margin-top: 2px;
    }

    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1.5px solid #ddd !important;
        font-size: 0.95rem !important;
        padding: 0.6rem 1rem !important;
    }

    .stButton > button {
        background: #111 !important;
        color: white !important;
        border-radius: 8px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
    }

    hr {
        border: none;
        border-top: 1px solid #ebebeb;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


api_key = st.secrets.get("GROQ_API_KEY", "")
if not api_key or api_key == "your_groq_api_key_here":
    st.warning("⚠️ **Groq API key not configured.** Please add your key to `.streamlit/secrets.toml`:\n\n```\nGROQ_API_KEY = \"gsk_your_actual_key\"\n```\n\nGet a free key at [console.groq.com](https://console.groq.com)")
    st.stop()

@st.cache_resource
def load_db_and_llm(_api_key):
    db = SQLDatabase.from_uri("sqlite:///startups.db")
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=_api_key
    )
    return db, llm

db, llm = load_db_and_llm(api_key)
schema = db.get_table_info()

prompt = ChatPromptTemplate.from_template("""
You are an expert SQL analyst working with an Indian startup funding database.

Schema:
{schema}

Rules:
- Use ONLY the tables and columns in the schema above
- Return ONLY the raw SQL query, nothing else
- No explanations, no markdown, no backticks
- For amounts, the column is funding_amount_usd_million (in USD millions)
- For company valuations, use valuation_usd_million

Question: {question}
""")

sql_chain = prompt | llm | StrOutputParser()

st.markdown('<div class="main-title">🚀 India Startup<br>Funding Explorer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask questions about Indian startup funding rounds in plain English — powered by Groq + LLaMA 3.3</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="stat-card"><div class="stat-number">40+</div><div class="stat-label">Funding Rounds</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-card"><div class="stat-number">35+</div><div class="stat-label">Startups</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-card"><div class="stat-number">8</div><div class="stat-label">Sectors</div></div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("**Try these examples:**")
examples = [
    "Which startups raised more than $300M?",
    "Top 5 startups by valuation",
    "How many Fintech startups are there?",
    "Which city has the most funded startups?",
    "Show all startups that raised in 2023",
    "Average funding by sector",
]

if "selected_example" not in st.session_state:
    st.session_state["selected_example"] = ""

def set_example(ex):
    st.session_state["selected_example"] = ex

cols = st.columns(3)
for i, example in enumerate(examples):
    with cols[i % 3]:
        st.button(example, key=f"ex_{i}", use_container_width=True, on_click=set_example, args=(example,))

st.markdown("<hr>", unsafe_allow_html=True)

question = st.text_input(
    "Ask your question:",
    value=st.session_state["selected_example"],
    placeholder="e.g. Which Bangalore startup raised the most money?",
    label_visibility="collapsed"
)

if question:
    with st.spinner("Thinking..."):
        try:
            sql_query = sql_chain.invoke({
                "schema": schema,
                "question": question
            }).strip().replace("```sql", "").replace("```", "").strip()

            st.markdown("**Generated SQL**")
            st.markdown(f'<div class="sql-box">{sql_query}</div>', unsafe_allow_html=True)

            result = db.run(sql_query)

            st.markdown("**Results**")
            if result:
                st.success(result)
            else:
                st.info("No results found for this query.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Built with LangChain · Groq · LLaMA 3.3 · Streamlit · SQLite | [GitHub](https://github.com) · Made by Chakresh")
