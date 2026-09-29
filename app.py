import os

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()


# ---------- Output schema ----------
class LogAnalysis(BaseModel):
    summary: str = Field(description="Overall summary of the application log")
    errors: list[str] = Field(description="Important errors found in the logs")
    warnings: list[str] = Field(description="Important warnings found in the logs")
    repeated_errors: list[str] = Field(description="Errors that occurred multiple times")
    possible_causes: list[str] = Field(description="Possible causes of the detected problems")
    suggestions: list[str] = Field(description="Practical troubleshooting suggestions")


# ---------- Prompt ----------
PROMPT = ChatPromptTemplate.from_template("""
You are an AI application log analyzer.

Analyze the provided application logs carefully.

Your tasks are:

1. Identify important errors.
2. Identify important warnings.
3. Identify errors that occur repeatedly.
4. Suggest possible causes for the detected problems.
5. Suggest practical troubleshooting steps.
6. Provide a concise overall summary.

The application has already calculated these statistics:

Total log entries: {total_entries}
Errors: {error_count}
Warnings: {warning_count}
Info messages: {info_count}

Important rules:

- Base your analysis only on the provided logs.
- Do not invent specific facts that are not present in the logs.
- Do not change the provided statistics.
- If there are no errors, return an empty list for errors.
- If there are no warnings, return an empty list for warnings.
- Focus on explaining the problems found in the logs.
- Keep troubleshooting suggestions practical and relevant.

Application Logs:

{logs}
""")


# ---------- Helpers ----------
def get_log_stats(log_text: str) -> dict:
    lines = [line.strip() for line in log_text.splitlines() if line.strip()]
    stats = {"total_entries": len(lines), "errors": 0, "warnings": 0, "info": 0}

    for line in lines:
        if " ERROR " in line:
            stats["errors"] += 1
        elif " WARNING " in line:
            stats["warnings"] += 1
        elif " INFO " in line:
            stats["info"] += 1
    return stats


@st.cache_resource
def get_chain(api_key: str):
    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0, api_key=api_key)
    return PROMPT | llm.with_structured_output(LogAnalysis)


def show_list(title: str, items: list[str], icon: str):
    items = list(dict.fromkeys(items))  # remove duplicates, keep order
    st.subheader(title)
    if items:
        for item in items:
            st.markdown(f"{icon} {item}")
    else:
        st.write("None found.")


# ---------- UI ----------
st.set_page_config(page_title="AI Log Analyzer", page_icon="🔍", layout="wide")
st.title("🔍 AI Log Analyzer")
st.caption("Upload or paste application logs and get an AI-powered analysis.")

api_key = os.getenv("GROQ_API_KEY") or st.sidebar.text_input(
    "Groq API key", type="password"
)

uploaded = st.file_uploader("Upload a log file", type=["log", "txt"])
pasted = st.text_area("...or paste logs here", height=200)

log_text = uploaded.read().decode("utf-8", errors="ignore") if uploaded else pasted

if st.button("Analyze Logs", type="primary"):
    if not api_key:
        st.error("Please provide your Groq API key.")
    elif not log_text.strip():
        st.warning("Please upload or paste some logs first.")
    else:
        stats = get_log_stats(log_text)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Entries", stats["total_entries"])
        c2.metric("Errors", stats["errors"])
        c3.metric("Warnings", stats["warnings"])
        c4.metric("Info", stats["info"])

        with st.spinner("Analyzing logs..."):
            try:
                result = get_chain(api_key).invoke(
                    {
                        "logs": log_text,
                        "total_entries": stats["total_entries"],
                        "error_count": stats["errors"],
                        "warning_count": stats["warnings"],
                        "info_count": stats["info"],
                    }
                )
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.stop()

        st.subheader("Summary")
        st.info(result.summary)

        left, right = st.columns(2)
        with left:
            show_list("Errors", result.errors, "🔴")
            show_list("Repeated Errors", result.repeated_errors, "🔁")
            show_list("Possible Causes", result.possible_causes, "🔍")
        with right:
            show_list("Warnings", result.warnings, "⚠️")
            show_list("Suggestions", result.suggestions, "🛠️")