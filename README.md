# 🩺 SQLRx – DocNexus AI 
**Natural Language to SQL for Healthcare Claims Analytics**

LLM-powered natural language to SQL for healthcare claims search. Supports multi-table joins, filters, and structured results. This prototype allows commercial teams to query healthcare claims data using natural language. Designed for scalability and healthcare-specific accuracy, it converts free-form questions into actionable SQL, supports interpretation, compliance checks, and intelligent refinement.

## Architecture Diagram

![SQLRx-DocSearchAI Architecture](assets/Architecture%20Diagram.png)


## 🧠 Architecture Highlights  
- **Agentic Workflow**: Built using **LangChain** for modular and scalable task delegation.  
- **Model-Agnostic LLM**: Gemini Flash used for dev; swappable with GPT-4 or Claude for better results.  
- **Database**: Lightweight **SQLite** backend (easily extendable to Postgres/Snowflake).  
- **RAG Support**: Schema ingested via text files or direct introspection to improve SQL generation.  
- **Auto Execution & Feedback**: Queries are run and errors/results are fed back for 2–3 retry loops.

## 🧰 Tech Stack  

| Component         | Tool/Library           |
|------------------|------------------------|
| Frontend UI       | Streamlit              |
| LLM Orchestration | LangChain + Python     |
| Language Models   | Gemini 2.5 Flash / GPT-4 |
| Backend DB        | SQLite (extensible)    |

## ✨ Key Features  
- 🔍 **Natural Language to SQL**  
- 🛡️ **Compliance Checks (HIPAA/PHI)**  
- ♻️ **Regenerate Query if Unsatisfied**  
- 📊 **Query Accuracy Metrics + Logging**  
- 💡 **Schema + Domain-Aware Interpretation**  
- ⚙️ **Direct DB Execution from UI**

## 📝 Notes & Assumptions  
- Domain concepts (ICD-10, CPT, HCP, etc.) are embedded into all prompt workflows  
- Schema is interpreted dynamically to adapt to structural changes  
- Prototype is privacy-aware with simplified PHI/PII validation  
- System is optimized for dev use but ready for enterprise scale-up

## 📸 Screenshots  
> See the `Documentation and Screenshots.pdf` for visuals of query generation, execution, compliance validation, and logging UI.

## 📂 Folder Structure

```
├── src/
│ ├── langchain_agents.py # Modular agent definitions
│ ├── streamlit_app.py # UI logic
│ └── utils/ # Helpers, schema loaders
├── config/ # Crew AI prototype (discarded)
├── vanna-ai/ # Vanna AI prototype (discarded)
├── SchemaNotes.txt # Optional schema hints
└── README.md
```
