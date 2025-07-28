# langchain_agents.py
import os
from dotenv import load_dotenv
load_dotenv()                         # loads .env into os.environ

from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
from utils.helper import calculate_gpt4o_mini_cost
import tiktoken

# ---------------- Gemini config ----------------
GEMINI_KEY = ""     # same .env file
MODEL_NAME = "gemini-2.5-flash"   # or gemini-2.0-flash [^45^]

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0.2,
    google_api_key=GEMINI_KEY
)

ENC = tiktoken.encoding_for_model("gpt-4o-mini")  # fallback tokenizer


def load_schema_notes(file_path: str = "SchemaNotes.txt") -> str:
    """Load schema notes from file with detailed column information"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "Schema notes file not found. Using basic schema information."
    except Exception as e:
        return f"Error loading schema notes: {e}"


def count_tokens(text: str) -> int:
    return len(ENC.encode(text))


def run_agent(system: str, human: str) -> Dict[str, Any]:
    messages = [SystemMessage(content=system), HumanMessage(content=human)]
    response = llm.invoke(messages)
    prompt_tokens = count_tokens(system + human)
    completion_tokens = count_tokens(str(response.content))
    cost = calculate_gpt4o_mini_cost(prompt_tokens, completion_tokens)
    text = "".join(str(item) for item in response.content).strip() if isinstance(response.content, list) else str(response.content).strip()
    return {"text": text, "cost": cost}


# ---------- Healthcare Domain Context ----------
HEALTHCARE_CONTEXT = """
Key Dataset Terms:
- ICD-10: International Classification of Diseases, 10th Revision standard diagnostic codes
- CPT: Current Procedural Terminology used to describe procedures and services
- HCP: Healthcare Professional includes doctors, specialists, NPs, etc.
- HCO: Healthcare Organization hospitals, health systems, clinics, ASCs, etc.
- Claim: A record of a billed interaction between a patient and provider for a service
- Patient: The individual receiving treatment or services
- Procedure: A medical operation or clinical service performed (e.g., surgery, screening)
- Drug: A prescribed or administered pharmaceutical product (e.g., Ozempic, Humira)
- Therapy Area: The medical area or specialty the product/procedure is targeting (e.g., endocrinology, cardiology)
- KOL: Key Opinion Leader highly influential HCPs often involved in research and education
- Trial: A clinical study registered in databases (e.g., ClinicalTrials.gov) used to evaluate drugs/devices
- NPI: National Provider Identifier  unique identification number for healthcare providers
- NDC: National Drug Code unique identifier for drug products
- AWP: Average Wholesale Price benchmark pricing for pharmaceuticals
- DAW: Dispense As Written prescription instruction codes
- Type 1 NPI: Individual healthcare provider identifier
- Type 2 NPI: Organization/group practice identifier

Table Context:
1. as_lsf_v1 (Payments to HCPs): Contains pharmaceutical company payments to healthcare providers
2. as_providers_v1 (Provider Details): Comprehensive provider information including specialties and locations
3. as_providers_referrals_v2 (Referral Patterns): Healthcare provider referral relationships and patterns
4. fct_pharmacy_clear_claim_allstatus_cluster_brand (Pharmacy Claims): Prescription claims data
5. mf_conditions (Condition Directory): Medical condition classifications and project mappings
6. mf_providers (KOL Providers): Key Opinion Leader provider profiles and ratings
7. mf_scores (KOL Scores): Performance scores for healthcare providers
"""

# ---------- the three agent helpers ----------
def generate_sql(user_input: str, db_schema: str) -> Dict[str, Any]:
    schema_notes = load_schema_notes()
    system = (
        "You are a highly skilled Senior Data Analyst specializing in healthcare SQL analytics. "
        "Your task is to generate a single, syntactically correct SQLite query that fulfills the user's request. "
        "Strictly use ONLY the tables and columns provided in the schema below. "
        "Do NOT use any tables, columns, or SQL features not present in the schema. "
        "Use the healthcare domain context and detailed schema notes to understand medical terminology and relationships. "
        "Pay special attention to the column descriptions and sample data provided in the schema notes. "
        "Return ONLY the SQL query, with no explanations or extra text."
    )
    human = (
        f"Healthcare Domain Context:\n{HEALTHCARE_CONTEXT}\n\n"
        f"Detailed Schema Notes:\n{schema_notes}\n\n"
        f"Database schema:\n{db_schema}\n\n"
        f"User request:\n{user_input}\n\n"
        "Remember: Only output the SQL query. Use healthcare domain knowledge and detailed column information to interpret requests correctly."
    )
    return run_agent(system, human)


def review_sql(sql: str, db_schema: str) -> Dict[str, Any]:
    schema_notes = load_schema_notes()
    system = (
        "You are an expert SQL Code Reviewer specializing in healthcare data analytics. "
        "Your job is to review the provided SQLite query for correctness, efficiency, and best practices. "
        "Consider healthcare-specific data patterns and relationships when optimizing queries. "
        "Use the detailed schema notes to understand column meanings and optimize joins and filters. "
        "If improvements can be made, return the optimized SQL query. "
        "If the query is already optimal, return it unchanged. "
        "Do NOT include explanations or comments—return ONLY the SQL query."
    )
    human = (
        f"Healthcare Domain Context:\n{HEALTHCARE_CONTEXT}\n\n"
        f"Detailed Schema Notes:\n{schema_notes}\n\n"
        f"Database schema:\n{db_schema}\n\n"
        f"SQL to review:\n{sql}\n\n"
        "Remember: Only output the SQL query. Consider healthcare data relationships and performance."
    )
    return run_agent(system, human)


def check_compliance(sql: str) -> Dict[str, Any]:
    system = (
        "You are a Healthcare Data Privacy and Compliance Officer. "
        "Analyze the provided SQL query for compliance with healthcare data privacy regulations (HIPAA, GDPR) and best practices. "
        "Check for potential exposure of PHI (Protected Health Information) or PII (Personally Identifiable Information). "
        "Consider healthcare-specific compliance requirements for provider data, patient data, and pharmaceutical information. "
        "Return a concise markdown report stating 'Compliant' if there are no issues, "
        "or list specific privacy or compliance violations if found. "
        "Be brief and clear, focusing on healthcare data protection."
    )
    human = (
        f"Healthcare Domain Context:\n{HEALTHCARE_CONTEXT}\n\n"
        f"SQL query to check:\n{sql}\n\n"
        "Respond with a short markdown report focusing on healthcare data privacy compliance."
    )
    return run_agent(system, human)


def interpret_healthcare_query(user_input: str, db_schema: str) -> Dict[str, Any]:
    """
    Enhanced function to interpret healthcare queries with domain-specific understanding
    """
    schema_notes = load_schema_notes()
    system = (
        "You are a Healthcare Data Analyst specializing in interpreting business questions into database queries. "
        "Your task is to understand the user's healthcare-related question and provide context about what data they're looking for. "
        "Identify relevant tables, columns, and relationships based on the schema notes and healthcare domain knowledge. "
        "Explain what the user is asking for in terms of the available data structure. "
        "Provide a clear interpretation without generating the actual SQL query."
    )
    human = (
        f"Healthcare Domain Context:\n{HEALTHCARE_CONTEXT}\n\n"
        f"Detailed Schema Notes:\n{schema_notes}\n\n"
        f"Database schema:\n{db_schema}\n\n"
        f"User request:\n{user_input}\n\n"
        "Please interpret this healthcare query and explain what data the user is looking for."
    )
    return run_agent(system, human)


def validate_healthcare_sql(sql: str, db_schema: str) -> Dict[str, Any]:
    """
    Validate SQL query against healthcare data schema and best practices
    """
    schema_notes = load_schema_notes()
    system = (
        "You are a Healthcare Database Validator. "
        "Your task is to validate the provided SQL query against the healthcare database schema. "
        "Check for: 1) Correct table and column names, 2) Proper joins and relationships, "
        "3) Healthcare-specific data handling, 4) Performance considerations. "
        "Return a validation report indicating if the query is valid and any issues found. "
        "Be specific about what needs to be corrected if issues are found."
    )
    human = (
        f"Healthcare Domain Context:\n{HEALTHCARE_CONTEXT}\n\n"
        f"Detailed Schema Notes:\n{schema_notes}\n\n"
        f"Database schema:\n{db_schema}\n\n"
        f"SQL query to validate:\n{sql}\n\n"
        "Please validate this query and provide a detailed report."
    )
    return run_agent(system, human)
