import streamlit as st
import sqlparse
import pandas as pd
from utils.db_simulator import get_structured_schema, run_query
from langchain_agents import generate_sql, review_sql, check_compliance, interpret_healthcare_query, validate_healthcare_sql
from utils.ui_helpers import display_metrics_dashboard, create_healthcare_context_help, display_query_examples
import time

# Page configuration
st.set_page_config(
    page_title="Healthcare SQL Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional healthcare theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0066cc 0%, #004499 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        color: white;
        border-radius: 0 0 15px 15px;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #0066cc;
    }
    
    .step-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    .step-header {
        color: #0066cc;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    
    .step-number {
        background: #0066cc;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
        font-weight: bold;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .sidebar-content {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .query-example {
        background: #e3f2fd;
        padding: 0.8rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 3px solid #2196f3;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .query-example:hover {
        background: #bbdefb;
    }
    
    .cost-display {
        background: #fff;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 2px solid #4caf50;
        color: #2e7d32;
        font-weight: bold;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

DB_PATH = "dataset/data.sqlite"

@st.cache_data(show_spinner=False)
def load_schema():
    return get_structured_schema(DB_PATH)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏥 DocNexus AI SQL Analytics Platform</h1>
    <p>AI-Powered Healthcare Data Analysis with Natural Language Processing</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced features
with st.sidebar:
    st.markdown("### 🚀 Quick Actions")
    
    # Schema management
    if st.button("🔄 Refresh Schema", use_container_width=True):
        st.cache_data.clear()
        st.success("Schema refreshed successfully!")
    
    # Database info
    db_schema = load_schema()
    st.markdown("### 📊 Database Overview")
    
    # Count tables
    table_count = db_schema.count("TABLE:")
    st.metric("📋 Tables", table_count)
    
    # Example queries with enhanced UI
    st.markdown("### 💡 Example Queries")
    
    selected_example = display_query_examples()
    if selected_example:
        st.session_state["example_query"] = selected_example
        st.rerun()
    
    # Healthcare context help
    create_healthcare_context_help()
    
    # Schema viewer
    with st.expander("📋 Database Schema"):
        st.code(db_schema, language="sql")

# Main content area
col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### 📈 Session Analytics")
    
    # Initialize session state
    session_keys = ["generated_sql", "reviewed_sql", "compliance_report", "query_result", "llm_cost", "interpretation", "validation"]
    for k in session_keys:
        if k not in st.session_state:
            st.session_state[k] = None if k != "llm_cost" else 0.0
    
    # Enhanced metrics dashboard
    steps_completed = sum(1 for key in session_keys[:-1] if st.session_state.get(key) is not None)
    display_metrics_dashboard(st.session_state['llm_cost'], steps_completed, len(session_keys)-1)
    
    # Progress indicators
    steps = [
        ("🔍", "Interpret Query", st.session_state["interpretation"] is not None),
        ("💻", "Generate SQL", st.session_state["generated_sql"] is not None),
        ("🔍", "Review SQL", st.session_state["reviewed_sql"] is not None),
        ("✅", "Validate", st.session_state["validation"] is not None),
        ("🔒", "Compliance", st.session_state["compliance_report"] is not None),
        ("🚀", "Execute", st.session_state["query_result"] is not None)
    ]
    
    st.markdown("### 📋 Progress")
    for icon, step, completed in steps:
        status = "✅" if completed else "⏳"
        st.markdown(f"{status} {icon} {step}")

with col1:
    st.markdown("### 🎯 Natural Language Query Interface")
    
    # Query input with example integration
    default_query = st.session_state.get("example_query", "")
    if default_query:
        del st.session_state["example_query"]
    
    prompt = st.text_area(
        "Enter your healthcare data question:",
        value=default_query,
        height=100,
        placeholder="e.g., Show me the top 10 providers by payment amounts from pharmaceutical companies..."
    )
    
    def add_cost(c):
        st.session_state["llm_cost"] += c
    
    # Enhanced button layout
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    
    with col_btn1:
        if st.button("🔍 Analyze Query", use_container_width=True) and prompt.strip():
            with st.spinner("Interpreting healthcare query..."):
                try:
                    interpretation = interpret_healthcare_query(prompt, db_schema)
                    st.session_state["interpretation"] = interpretation["text"]
                    add_cost(interpretation["cost"])
                    st.success("Query interpretation completed!")
                except Exception as e:
                    st.error(f"Error interpreting query: {e}")
    
    with col_btn2:
        if st.button("💻 Generate SQL", use_container_width=True) and prompt.strip():
            with st.spinner("Generating SQL query..."):
                try:
                    gen = generate_sql(prompt, db_schema)
                    st.session_state["generated_sql"] = gen["text"]
                    add_cost(gen["cost"])
                    st.success("SQL generated successfully!")
                except Exception as e:
                    st.error(f"Error generating SQL: {e}")
    
    with col_btn3:
        if st.button("📋 View Schema", use_container_width=True):
            st.session_state["show_schema"] = not st.session_state.get("show_schema", False)
            st.rerun()
    
    with col_btn4:
        if st.button("🔄 Reset All", use_container_width=True):
            for k in session_keys:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

    # Display database schema if requested
    if st.session_state.get("show_schema", False):
        st.markdown("""
        <div class="step-container">
            <div class="step-header">
                <div class="step-number">📋</div>
                🗂️ Database Schema Overview
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different schema views
        tab1, tab2, tab3 = st.tabs(["📊 Structured View", "🔍 Raw Schema", "📋 Table Summary"])
        
        with tab1:
            st.markdown("#### 🏥 Healthcare Database Structure")
            
            # Parse and display schema in a more readable format
            tables = []
            current_table = None
            
            for line in db_schema.split('\n'):
                if line.startswith('TABLE:'):
                    current_table = line.replace('TABLE:', '').strip()
                    tables.append(current_table)
            
            # Display tables in a nice grid
            if tables:
                st.markdown("**Available Tables:**")
                cols = st.columns(3)
                for i, table in enumerate(tables):
                    with cols[i % 3]:
                        st.markdown(f"🗂️ **{table}**")
                
                # Allow user to select a table for detailed view
                selected_table = st.selectbox(
                    "Select a table to view details:",
                    [""] + tables,
                    format_func=lambda x: "Choose a table..." if x == "" else f"📋 {x}"
                )
                
                if selected_table:
                    st.markdown(f"#### 📋 Table Details: {selected_table}")
                    
                    # Extract table details from schema
                    table_found = False
                    table_details = []
                    
                    for line in db_schema.split('\n'):
                        if f'TABLE: {selected_table}' in line:
                            table_found = True
                            continue
                        elif table_found and line.startswith('TABLE:'):
                            break
                        elif table_found and line.strip():
                            table_details.append(line)
                    
                    if table_details:
                        st.code('\n'.join(table_details), language="sql")
        
        with tab2:
            st.markdown("#### 🔍 Complete Raw Schema")
            st.code(db_schema, language="sql")
        
        with tab3:
            st.markdown("#### 📋 Quick Table Summary")
            
            # Healthcare table descriptions
            table_descriptions = {
                "as_lsf_payments": "💊 **Pharmaceutical Payments**: Payments from life science firms to healthcare providers",
                "as_providers": "👩‍⚕️ **Provider Details**: Comprehensive healthcare provider information and specialties",
                "as_providers_referrals": "🔗 **Referral Patterns**: Healthcare provider referral relationships and networks",
                "fct_pharmacy_claims": "💉 **Pharmacy Claims**: Prescription claims and pharmaceutical dispensing data",
                "mf_conditions": "🏥 **Medical Conditions**: Directory of medical conditions and classifications",
                "mf_providers": "⭐ **KOL Providers**: Key Opinion Leader provider profiles and ratings",
                "mf_scores": "📊 **Provider Scores**: Performance scores and metrics for healthcare providers"
            }
            
            # Display table descriptions
            for table_name, description in table_descriptions.items():
                if table_name in db_schema:
                    st.markdown(f"- {description}")
            
            # Quick statistics
            st.markdown("---")
            st.markdown("**📊 Schema Statistics:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📋 Total Tables", len(tables))
            
            with col2:
                # Count total columns (approximate)
                column_count = db_schema.count("INTEGER") + db_schema.count("TEXT") + db_schema.count("REAL")
                st.metric("📊 Total Columns", column_count)
            
            with col3:
                # Count foreign keys
                fk_count = db_schema.count("FOREIGN KEY")
                st.metric("🔗 Foreign Keys", fk_count)

    # Display interpretation if available
    if st.session_state["interpretation"]:
        st.markdown("""
        <div class="step-container">
            <div class="step-header">
                <div class="step-number">1</div>
                🔍 Query Interpretation
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(st.session_state["interpretation"])

# SQL Generation and Processing
if st.session_state["generated_sql"]:
    st.markdown("""
    <div class="step-container">
        <div class="step-header">
            <div class="step-number">2</div>
            💻 Generated SQL Query
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.code(sqlparse.format(st.session_state["generated_sql"], reindent=True, keyword_case="upper"), language="sql")
    
    # Action buttons for SQL processing
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✅ Review & Validate", use_container_width=True):
            with st.spinner("Reviewing and validating SQL..."):
                try:
                    # Review SQL
                    rev = review_sql(st.session_state["generated_sql"], db_schema)
                    st.session_state["reviewed_sql"] = rev["text"]
                    add_cost(rev["cost"])
                    
                    # Validate SQL
                    validation = validate_healthcare_sql(st.session_state["reviewed_sql"], db_schema)
                    st.session_state["validation"] = validation["text"]
                    add_cost(validation["cost"])
                    
                    # Check compliance
                    comp = check_compliance(st.session_state["reviewed_sql"])
                    st.session_state["compliance_report"] = comp["text"]
                    add_cost(comp["cost"])
                    
                    st.success("SQL reviewed and validated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error in review process: {e}")
    
    with col2:
        if st.button("🔄 Regenerate", use_container_width=True):
            st.session_state["generated_sql"] = None
            st.session_state["reviewed_sql"] = None
            st.session_state["validation"] = None
            st.session_state["compliance_report"] = None
            st.session_state["query_result"] = None
            st.rerun()
    
    with col3:
        if st.button("❌ Clear Results", use_container_width=True):
            for k in ["reviewed_sql", "validation", "compliance_report", "query_result"]:
                if k in st.session_state:
                    st.session_state[k] = None
            st.rerun()

# Display reviewed SQL and validation
if st.session_state["reviewed_sql"]:
    st.markdown("""
    <div class="step-container">
        <div class="step-header">
            <div class="step-number">3</div>
            🔍 Reviewed & Optimized SQL
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.code(sqlparse.format(st.session_state["reviewed_sql"], reindent=True, keyword_case="upper"), language="sql")
    
    # Display validation results
    if st.session_state["validation"]:
        st.markdown("""
        <div class="step-container">
            <div class="step-header">
                <div class="step-number">4</div>
                ✅ Validation Report
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(st.session_state["validation"])

# Display compliance report
if st.session_state["compliance_report"]:
    st.markdown("""
    <div class="step-container">
        <div class="step-header">
            <div class="step-number">5</div>
            🔒 Compliance Check
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    compliance_text = st.session_state["compliance_report"]
    
    if "compliant" in compliance_text.lower():
        st.markdown(f"""
        <div class="success-box">
            <strong>✅ Compliance Status: PASSED</strong><br>
            {compliance_text}
        </div>
        """, unsafe_allow_html=True)
        
        # Execute query button
        if st.button("🚀 Execute Query", use_container_width=True):
            with st.spinner("Executing query..."):
                try:
                    result = run_query(st.session_state["reviewed_sql"])
                    st.session_state["query_result"] = result
                    st.success("Query executed successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Query execution failed: {e}")
    else:
        st.markdown(f"""
        <div class="error-box">
            <strong>❌ Compliance Status: FAILED</strong><br>
            {compliance_text}
        </div>
        """, unsafe_allow_html=True)

# Display query results
if st.session_state["query_result"]:
    st.markdown("""
    <div class="step-container">
        <div class="step-header">
            <div class="step-number">6</div>
            📊 Query Results
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Try to parse as DataFrame for better display
    try:
        import io
        from contextlib import redirect_stdout
        
        # Check if result looks like a table
        if "Query Results:" in st.session_state["query_result"]:
            result_text = st.session_state["query_result"].replace("Query Results:\n", "")
            
            # Try to display as a nice table
            lines = result_text.strip().split('\n')
            if len(lines) > 1:
                # Display as formatted table
                st.markdown("### 📋 Data Table")
                st.text(result_text)
            else:
                st.code(st.session_state["query_result"])
        else:
            st.code(st.session_state["query_result"])
    except Exception:
        st.code(st.session_state["query_result"])
    
    # Download results
    if st.download_button(
        label="📥 Download Results",
        data=st.session_state["query_result"],
        file_name="query_results.txt",
        mime="text/plain",
        use_container_width=True
    ):
        st.success("Results downloaded!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🏥 DocNexux AI SQL Analytics Platform | Powered by AI & LangChain</p>
    <p>Built for secure, compliant healthcare data analysis</p>
</div>
""", unsafe_allow_html=True)