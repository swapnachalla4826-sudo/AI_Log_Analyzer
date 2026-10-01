# 🔍 AI Application Log Analyzer

An AI-powered Streamlit application that analyzes application logs, identifies errors and warnings, detects repeated problems, suggests possible causes, and provides practical troubleshooting recommendations.

## Overview

```text
Log File / Pasted Logs
        ↓
Log Statistics
        ↓
Prompt + Statistics + Logs
        ↓
Groq LLM
        ↓
Structured LogAnalysis
        ↓
Summary / Errors / Warnings / Causes / Suggestions
```

## Features

- Upload `.log` or `.txt` files
- Paste logs directly
- Count total entries
- Count errors, warnings, and info messages
- Identify important errors
- Identify important warnings
- Find repeated errors
- Suggest possible causes
- Generate troubleshooting recommendations
- Display structured results in Streamlit

## Structured Output

The application uses a Pydantic schema containing:

```text
summary
errors
warnings
repeated_errors
possible_causes
suggestions
```

The LLM is explicitly instructed to use only the supplied logs and preserve the already-calculated statistics. fileciteturn3file8

## LangChain Workflow

```text
ChatPromptTemplate
       ↓
ChatGroq
       ↓
Structured Output
       ↓
Pydantic LogAnalysis
```

The current application uses `openai/gpt-oss-20b` through Groq with temperature `0`.

## Log Statistics

The parser counts non-empty lines and recognizes the log levels:

```text
 ERROR 
 WARNING 
 INFO 
```

## Tech Stack

- Python
- Streamlit
- LangChain
- LangChain Groq
- Pydantic
- Groq
- Structured Output
- Prompt Engineering

## Installation

```bash
pip install streamlit langchain-groq langchain-core pydantic python-dotenv
```

Set your API key:

```text
GROQ_API_KEY=your_api_key_here
```

Never commit API keys to GitHub.

## Run

```bash
streamlit run app.py
```

## Applications

- Production log analysis
- Debugging assistance
- Error triage
- Incident investigation
- Developer productivity
- Application monitoring

## Limitations

The current parser expects conventional `ERROR`, `WARNING`, and `INFO` tokens. Custom log formats may require additional parsing logic. AI-generated causes and recommendations should be verified against the actual application and infrastructure.

## Future Improvements

- JSON-log support
- Error clustering
- Embedding-based similarity
- Anomaly detection
- Historical log comparison
- RAG over application documentation
- Agentic troubleshooting workflows

## Author

**Challa Swapna**
