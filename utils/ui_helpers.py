"""
Enhanced Streamlit app utilities for healthcare SQL analytics
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any

def display_metrics_dashboard(cost: float, steps_completed: int, total_steps: int):
    """Display a metrics dashboard"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="💰 Total Cost",
            value=f"${cost:.6f}",
            delta=f"${cost:.6f}" if cost > 0 else None
        )
    
    with col2:
        st.metric(
            label="📊 Progress",
            value=f"{steps_completed}/{total_steps}",
            delta=f"{(steps_completed/total_steps)*100:.1f}%"
        )
    
    with col3:
        efficiency_score = max(0, 100 - (cost * 10000))  # Mock efficiency calculation
        st.metric(
            label="⚡ Efficiency",
            value=f"{efficiency_score:.1f}%",
            delta=f"{'High' if efficiency_score > 80 else 'Medium' if efficiency_score > 50 else 'Low'}"
        )

def create_progress_bar(steps: List[Dict[str, Any]]) -> None:
    """Create a visual progress bar for the SQL generation process"""
    
    completed_steps = sum(1 for step in steps if step['completed'])
    total_steps = len(steps)
    
    progress_percent = completed_steps / total_steps
    
    # Create progress bar
    st.markdown("### 🔄 Processing Pipeline")
    st.progress(progress_percent)
    
    # Create step indicators
    cols = st.columns(total_steps)
    for i, (col, step) in enumerate(zip(cols, steps)):
        with col:
            if step['completed']:
                st.markdown(f"✅ **{step['name']}**")
            elif i == completed_steps:
                st.markdown(f"⏳ **{step['name']}**")
            else:
                st.markdown(f"⏸️ {step['name']}")

def format_sql_with_highlighting(sql: str) -> str:
    """Format SQL with syntax highlighting"""
    try:
        import sqlparse
        return sqlparse.format(sql, reindent=True, keyword_case="upper")
    except ImportError:
        return sql

def create_healthcare_context_help():
    """Create a comprehensive help section for healthcare terms"""
    
    with st.expander("🏥 Healthcare Analytics Guide"):
        
        tab1, tab2, tab3 = st.tabs(["📚 Key Terms", "🗂️ Data Tables", "💡 Query Tips"])
        
        with tab1:
            st.markdown("""
            #### Healthcare Terminology
            
            **Provider Identifiers:**
            - **NPI (National Provider Identifier)**: Unique 10-digit ID for healthcare providers
            - **Type 1 NPI**: Individual healthcare professional
            - **Type 2 NPI**: Healthcare organization/group
            
            **Medical Coding:**
            - **ICD-10**: International Classification of Diseases (diagnosis codes)
            - **CPT**: Current Procedural Terminology (procedure codes)
            - **NDC**: National Drug Code (medication identifier)
            
            **Healthcare Entities:**
            - **HCP**: Healthcare Professional (doctors, nurses, specialists)
            - **HCO**: Healthcare Organization (hospitals, clinics)
            - **KOL**: Key Opinion Leader (influential healthcare professionals)
            
            **Pharmaceutical:**
            - **AWP**: Average Wholesale Price
            - **DAW**: Dispense As Written
            - **Therapy Area**: Medical specialty (cardiology, oncology, etc.)
            """)
        
        with tab2:
            st.markdown("""
            #### Available Data Tables
            
            **Payment Data:**
            - `as_lsf_payments`: Pharmaceutical company payments to providers
            
            **Provider Information:**
            - `as_providers`: Healthcare provider details and specialties
            - `mf_providers`: Key Opinion Leader profiles
            - `mf_scores`: Provider performance scores
            
            **Clinical Data:**
            - `as_providers_referrals`: Provider referral patterns
            - `fct_pharmacy_claims`: Prescription claims data
            - `mf_conditions`: Medical condition directory
            """)
        
        with tab3:
            st.markdown("""
            #### Query Writing Tips
            
            **Effective Queries:**
            - Be specific about time periods: "in 2023", "last year"
            - Use clear metrics: "total payments", "top 10", "average amount"
            - Specify provider types: "cardiologists", "primary care", "specialists"
            
            **Example Patterns:**
            - "Show me [metric] for [entity] in [time period]"
            - "Find [providers/drugs/conditions] with [criteria]"
            - "Compare [A] vs [B] by [metric]"
            
            **Common Analyses:**
            - Payment analysis by company/provider/specialty
            - Prescription trends and patterns
            - Provider performance and referral networks
            - Geographic distribution of healthcare services
            """)

def display_query_examples():
    """Display interactive query examples"""
    
    st.markdown("### 💡 Query Examples")
    
    categories = {
        "💊 Pharmaceutical Payments": [
            "Top 10 providers by total payment amounts",
            "Payments from ABBVIE to cardiology specialists",
            "Average payment per provider by pharmaceutical company",
            "Providers receiving payments for multiple therapy areas"
        ],
        "👩‍⚕️ Provider Analysis": [
            "KOL providers with highest scores in oncology",
            "Providers with multiple specialties and locations",
            "Referral patterns between primary care and specialists",
            "Geographic distribution of healthcare providers"
        ],
        "💉 Pharmacy & Prescriptions": [
            "Most prescribed medications by volume",
            "High-value pharmacy claims analysis",
            "Prescription patterns by diagnosis code",
            "Drug utilization trends over time"
        ],
        "📊 Healthcare Analytics": [
            "Provider performance metrics by specialty",
            "Condition prevalence and treatment patterns",
            "Healthcare spending analysis by region",
            "Quality metrics and outcome indicators"
        ]
    }
    
    for category, queries in categories.items():
        with st.expander(category):
            for query in queries:
                if st.button(f"📝 {query}", key=f"example_{hash(query)}"):
                    return query
    
    return None

def create_results_visualization(query_result: str):
    """Create visualizations for query results if possible"""
    
    if not query_result or "Query Results:" not in query_result:
        return
    
    try:
        # Extract table data from query result
        result_text = query_result.replace("Query Results:\n", "").strip()
        lines = result_text.split('\n')
        
        if len(lines) > 2:  # Has header and data
            # Try to create a simple chart
            st.markdown("### 📊 Visual Analysis")
            
            # For now, just show the text nicely formatted
            st.markdown("*Chart visualization would appear here for numerical data*")
            
    except Exception as e:
        pass  # Skip visualization if parsing fails
