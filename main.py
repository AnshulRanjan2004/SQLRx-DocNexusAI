# main.py
from utils.db_simulator import get_structured_schema, run_query, DB_PATH
from langchain_agents import (
    generate_sql, 
    review_sql, 
    check_compliance, 
    interpret_healthcare_query,
    validate_healthcare_sql
)

def main():
    """Enhanced main function with healthcare-aware SQL generation"""
    
    print("🏥 Healthcare SQL Analytics System")
    print("=" * 50)
    
    # Load database schema
    db_schema = get_structured_schema(DB_PATH)
    print(f"✅ Database schema loaded successfully")
    
    # Healthcare-focused example queries
    healthcare_queries = [
        "Show me the top 5 pharmaceutical companies by total payment amounts to providers",
        "Find all providers in cardiology specialty who received payments in 2023",
        "List the most prescribed drugs by total dispensed quantity",
        "Show referral patterns between specialists and primary care physicians",
        "Find KOL providers with highest scores for diabetes conditions"
    ]
    
    print("\n📋 Available Healthcare Queries:")
    for i, query in enumerate(healthcare_queries, 1):
        print(f"{i}. {query}")
    
    while True:
        print("\n" + "="*60)
        choice = input("\nEnter query number (1-5) or 'custom' for custom query, 'q' to quit: ").strip()
        
        if choice.lower() == 'q':
            break
        elif choice.lower() == 'custom':
            user_prompt = input("Enter your healthcare query: ").strip()
        elif choice.isdigit() and 1 <= int(choice) <= len(healthcare_queries):
            user_prompt = healthcare_queries[int(choice) - 1]
        else:
            print("❌ Invalid choice. Please try again.")
            continue
        
        if not user_prompt:
            print("❌ Empty query. Please try again.")
            continue
        
        print(f"\n🔍 Processing query: {user_prompt}")
        print("-" * 60)
        
        try:
            # 1. Interpret the healthcare query
            print("📖 Interpreting healthcare query...")
            interpretation = interpret_healthcare_query(user_prompt, db_schema)
            print(f"Interpretation: {interpretation['text']}")
            
            # 2. Generate SQL
            print("\n💻 Generating SQL...")
            gen = generate_sql(user_prompt, db_schema)
            raw_sql = gen["text"]
            print(f"Generated SQL:\n{raw_sql}")
            
            # 3. Review SQL
            print("\n🔍 Reviewing SQL...")
            rev = review_sql(raw_sql, db_schema)
            reviewed_sql = rev["text"]
            print(f"Reviewed SQL:\n{reviewed_sql}")
            
            # 4. Validate SQL
            print("\n✅ Validating SQL...")
            validation = validate_healthcare_sql(reviewed_sql, db_schema)
            print(f"Validation Report:\n{validation['text']}")
            
            # 5. Check compliance
            print("\n🔒 Checking compliance...")
            comp = check_compliance(reviewed_sql)
            compliance_report = comp["text"]
            print(f"Compliance Report:\n{compliance_report}")
            
            # 6. Execute query if compliant
            if "compliant" in compliance_report.lower():
                print("\n🚀 Executing query...")
                try:
                    result = run_query(reviewed_sql)
                    print(f"Query Results:\n{result}")
                except Exception as e:
                    print(f"❌ Query execution failed: {e}")
            else:
                print("⚠️  Query failed compliance check. Not executing.")
            
            # Show costs
            total_cost = gen["cost"] + rev["cost"] + comp["cost"] + interpretation["cost"] + validation["cost"]
            print(f"\n💰 Total LLM cost: ${total_cost:.6f}")
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()