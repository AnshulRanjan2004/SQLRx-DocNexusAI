#!/usr/bin/env python3
"""
Test script to demonstrate healthcare-aware SQL generation with enhanced context
"""

from langchain_agents import (
    generate_sql, 
    review_sql, 
    check_compliance, 
    interpret_healthcare_query,
    validate_healthcare_sql
)
from utils.db_simulator import get_structured_schema, DB_PATH

def test_healthcare_agents():
    """Test the enhanced healthcare-aware agents"""
    
    print("🏥 Healthcare SQL Agent Testing")
    print("=" * 50)
    
    # Get database schema
    db_schema = get_structured_schema(DB_PATH)
    print(f"Database Schema loaded: {len(db_schema)} characters")
    
    # Test queries
    test_queries = [
        "Find all providers who received payments from ABBVIE for diabetes-related products",
        "Show the top 5 KOL providers by score for cardiovascular conditions",
        "List all pharmacy claims for patients with diabetes in 2023",
        "Find referral patterns between cardiologists and primary care physicians",
        "Show payment amounts by pharmaceutical company and therapeutic area"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test Query {i}: {query}")
        print("-" * 60)
        
        # 1. Interpret the query
        print("🔍 Interpreting healthcare query...")
        interpretation = interpret_healthcare_query(query, db_schema)
        print(f"Interpretation: {interpretation['text'][:200]}...")
        
        # 2. Generate SQL
        print("\n💻 Generating SQL...")
        sql_result = generate_sql(query, db_schema)
        generated_sql = sql_result['text']
        print(f"Generated SQL:\n{generated_sql}")
        
        # 3. Review SQL
        print("\n🔍 Reviewing SQL...")
        review_result = review_sql(generated_sql, db_schema)
        reviewed_sql = review_result['text']
        print(f"Reviewed SQL:\n{reviewed_sql}")
        
        # 4. Validate SQL
        print("\n✅ Validating SQL...")
        validation_result = validate_healthcare_sql(reviewed_sql, db_schema)
        print(f"Validation: {validation_result['text'][:200]}...")
        
        # 5. Check compliance
        print("\n🔒 Checking compliance...")
        compliance_result = check_compliance(reviewed_sql)
        print(f"Compliance: {compliance_result['text']}")
        
        # Show costs
        total_cost = sql_result['cost'] + review_result['cost'] + compliance_result['cost']
        print(f"\n💰 Total Cost: ${total_cost:.4f}")
        
        print("\n" + "="*80)

if __name__ == "__main__":
    test_healthcare_agents()
