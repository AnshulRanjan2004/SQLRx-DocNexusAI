import sqlite3
import pandas as pd

DB_PATH = "dataset/data.sqlite"

# def setup_sample_db():
#     # Fixed: Use the correct DB_PATH instead of hardcoded filename
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # Drop tables if they exist (for repeatability in dev)
#     cursor.execute("DROP TABLE IF EXISTS transactions;")
#     cursor.execute("DROP TABLE IF EXISTS portfolios;")
#     cursor.execute("DROP TABLE IF EXISTS securities;")
#     cursor.execute("DROP TABLE IF EXISTS accounts;")
#     cursor.execute("DROP TABLE IF EXISTS clients;")
#     cursor.execute("DROP TABLE IF EXISTS advisors;")
#     cursor.execute("DROP TABLE IF EXISTS departments;")

#     # Create financial firm tables
#     cursor.execute("""
#         CREATE TABLE departments (
#             department_id INTEGER PRIMARY KEY,
#             department_name TEXT,
#             location TEXT
#         );
#     """)
    
#     cursor.execute("""
#         CREATE TABLE advisors (
#             advisor_id INTEGER PRIMARY KEY,
#             name TEXT,
#             email TEXT,
#             department_id INTEGER,
#             hire_date TEXT,
#             license_number TEXT,
#             FOREIGN KEY(department_id) REFERENCES departments(department_id)
#         );
#     """)
    
#     cursor.execute("""
#         CREATE TABLE clients (
#             client_id INTEGER PRIMARY KEY,
#             name TEXT,
#             email TEXT,
#             phone TEXT,
#             address TEXT,
#             advisor_id INTEGER,
#             onboarding_date TEXT,
#             risk_tolerance TEXT,
#             FOREIGN KEY(advisor_id) REFERENCES advisors(advisor_id)
#         );
#     """)
    
#     cursor.execute("""
#         CREATE TABLE accounts (
#             account_id INTEGER PRIMARY KEY,
#             client_id INTEGER,
#             account_type TEXT,
#             account_number TEXT,
#             balance REAL,
#             created_date TEXT,
#             status TEXT,
#             FOREIGN KEY(client_id) REFERENCES clients(client_id)
#         );
#     """)
    
#     cursor.execute("""
#         CREATE TABLE securities (
#             security_id INTEGER PRIMARY KEY,
#             symbol TEXT,
#             name TEXT,
#             security_type TEXT,
#             sector TEXT,
#             current_price REAL,
#             last_updated TEXT
#         );
#     """)
    
#     cursor.execute("""
#         CREATE TABLE portfolios (
#             portfolio_id INTEGER PRIMARY KEY,
#             account_id INTEGER,
#             security_id INTEGER,
#             shares REAL,
#             purchase_price REAL,
#             purchase_date TEXT,
#             FOREIGN KEY(account_id) REFERENCES accounts(account_id),
#             FOREIGN KEY(security_id) REFERENCES securities(security_id)
#         );
#     """)
    
#     cursor.execute("""
#         CREATE TABLE transactions (
#             transaction_id INTEGER PRIMARY KEY,
#             account_id INTEGER,
#             security_id INTEGER,
#             transaction_type TEXT,
#             shares REAL,
#             price_per_share REAL,
#             total_amount REAL,
#             transaction_date TEXT,
#             fee REAL,
#             FOREIGN KEY(account_id) REFERENCES accounts(account_id),
#             FOREIGN KEY(security_id) REFERENCES securities(security_id)
#         );
#     """)

#     # Populate with mock data
#     cursor.executemany("INSERT INTO departments VALUES (?, ?, ?);", [
#         (1, 'Wealth Management', 'New York'),
#         (2, 'Investment Banking', 'New York'),
#         (3, 'Research', 'Chicago'),
#         (4, 'Risk Management', 'Boston'),
#         (5, 'Operations', 'Dallas')
#     ])
    
#     cursor.executemany("INSERT INTO advisors VALUES (?, ?, ?, ?, ?, ?);", [
#         (1, 'John Smith', 'j.smith@financialfirm.com', 1, '2020-03-15', 'CFA-12345'),
#         (2, 'Sarah Johnson', 's.johnson@financialfirm.com', 1, '2019-08-22', 'CFP-67890'),
#         (3, 'Michael Chen', 'm.chen@financialfirm.com', 2, '2021-01-10', 'CFA-54321'),
#         (4, 'Emily Davis', 'e.davis@financialfirm.com', 3, '2018-11-05', 'CFA-98765'),
#         (5, 'Robert Wilson', 'r.wilson@financialfirm.com', 1, '2022-06-30', 'CFP-11223')
#     ])
    
#     cursor.executemany("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?);", [
#         (1, 'Alice Thompson', 'alice.thompson@email.com', '555-0101', '123 Main St, NY', 1, '2023-01-15', 'Moderate'),
#         (2, 'Bob Martinez', 'bob.martinez@email.com', '555-0102', '456 Oak Ave, CA', 1, '2023-02-20', 'Conservative'),
#         (3, 'Carol Williams', 'carol.williams@email.com', '555-0103', '789 Pine Rd, TX', 2, '2023-03-10', 'Aggressive'),
#         (4, 'David Brown', 'david.brown@email.com', '555-0104', '321 Elm St, FL', 3, '2023-04-05', 'Moderate'),
#         (5, 'Emma Jones', 'emma.jones@email.com', '555-0105', '654 Maple Dr, IL', 2, '2023-05-12', 'Conservative')
#     ])
    
#     cursor.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?);", [
#         (1, 1, 'Investment', 'INV-001-2023', 125000.00, '2023-01-15', 'Active'),
#         (2, 1, 'Retirement', 'RET-001-2023', 89000.00, '2023-01-15', 'Active'),
#         (3, 2, 'Investment', 'INV-002-2023', 75000.00, '2023-02-20', 'Active'),
#         (4, 3, 'Investment', 'INV-003-2023', 250000.00, '2023-03-10', 'Active'),
#         (5, 4, 'Investment', 'INV-004-2023', 180000.00, '2023-04-05', 'Active'),
#         (6, 5, 'Retirement', 'RET-005-2023', 95000.00, '2023-05-12', 'Active')
#     ])
    
#     cursor.executemany("INSERT INTO securities VALUES (?, ?, ?, ?, ?, ?, ?);", [
#         (1, 'AAPL', 'Apple Inc.', 'Stock', 'Technology', 185.50, '2024-04-30'),
#         (2, 'GOOGL', 'Alphabet Inc.', 'Stock', 'Technology', 2750.00, '2024-04-30'),
#         (3, 'MSFT', 'Microsoft Corp.', 'Stock', 'Technology', 420.00, '2024-04-30'),
#         (4, 'SPY', 'SPDR S&P 500 ETF', 'ETF', 'Diversified', 518.00, '2024-04-30'),
#         (5, 'BND', 'Vanguard Total Bond Market ETF', 'ETF', 'Fixed Income', 82.50, '2024-04-30'),
#         (6, 'AMZN', 'Amazon.com Inc.', 'Stock', 'Consumer Discretionary', 3200.00, '2024-04-30'),
#         (7, 'TSLA', 'Tesla Inc.', 'Stock', 'Consumer Discretionary', 800.00, '2024-04-30')
#     ])
    
#     cursor.executemany("INSERT INTO portfolios VALUES (?, ?, ?, ?, ?, ?);", [
#         (1, 1, 1, 100.0, 175.00, '2023-02-01'),
#         (2, 1, 4, 50.0, 500.00, '2023-02-01'),
#         (3, 1, 5, 200.0, 80.00, '2023-02-15'),
#         (4, 2, 4, 80.0, 495.00, '2023-02-01'),
#         (5, 3, 2, 10.0, 2600.00, '2023-03-01'),
#         (6, 3, 3, 25.0, 400.00, '2023-03-01'),
#         (7, 4, 1, 200.0, 180.00, '2023-03-15'),
#         (8, 4, 6, 15.0, 3100.00, '2023-03-15'),
#         (9, 5, 7, 50.0, 750.00, '2023-04-10'),
#         (10, 6, 5, 300.0, 81.00, '2023-05-15')
#     ])
    
#     cursor.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", [
#         (1, 1, 1, 'BUY', 100.0, 175.00, 17500.00, '2023-02-01', 9.99),
#         (2, 1, 4, 'BUY', 50.0, 500.00, 25000.00, '2023-02-01', 9.99),
#         (3, 1, 5, 'BUY', 200.0, 80.00, 16000.00, '2023-02-15', 9.99),
#         (4, 2, 4, 'BUY', 80.0, 495.00, 39600.00, '2023-02-01', 9.99),
#         (5, 3, 2, 'BUY', 10.0, 2600.00, 26000.00, '2023-03-01', 9.99),
#         (6, 3, 3, 'BUY', 25.0, 400.00, 10000.00, '2023-03-01', 9.99),
#         (7, 4, 1, 'BUY', 200.0, 180.00, 36000.00, '2023-03-15', 9.99),
#         (8, 4, 6, 'BUY', 15.0, 3100.00, 46500.00, '2023-03-15', 9.99),
#         (9, 5, 7, 'BUY', 50.0, 750.00, 37500.00, '2023-04-10', 9.99),
#         (10, 6, 5, 'BUY', 300.0, 81.00, 24300.00, '2023-05-15', 9.99),
#         (11, 1, 1, 'SELL', 25.0, 185.50, 4637.50, '2024-04-20', 9.99),
#         (12, 4, 7, 'BUY', 30.0, 800.00, 24000.00, '2024-04-25', 9.99)
#     ])

#     conn.commit()
#     conn.close()
#     print("Sample database created successfully.")

import re

def run_query(query: str) -> str:
# 1️⃣ Remove any leading/trailing junk (markdown fences, stray words, etc.)
    query = re.sub(r'(?is)^\s*```(?:sql)?\s*', '', query)  # leading ```sql
    query = re.sub(r'(?is)\s*```\s*$', '', query)         # trailing ```
    query = query.strip()                                 # remove leading/trailing whitespace

    # 2️⃣ If the first token is not a valid SQL keyword, drop it
    tokens = query.split()
    if tokens and tokens[0].lower() not in {"select", "insert", "update", "delete", "with"}:
        query = " ".join(tokens[1:]).lstrip()

    # 3️⃣ Execute the cleaned SQL
    try:
        import sqlite3, pandas as pd
        conn = sqlite3.connect("dataset/data.sqlite")
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.head().to_string(index=False)
    except Exception as e:
        return f"Query failed: {e}"

def get_db_schema(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        schema = ""
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name, in tables:
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            create_stmt = cursor.fetchone()[0]
            schema += create_stmt + ";\n\n"
        conn.close()
        return schema
    except Exception as e:
        return f"Error retrieving schema: {e}"

def get_structured_schema(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("Retrieving structured schema...")
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            return "No tables found in the database. Make sure the database exists and has been created."
        
        lines = ["=== DATABASE SCHEMA ===\n"]
        
        for table_name, in tables:
            lines.append(f"TABLE: {table_name}")
            lines.append("-" * (len(table_name) + 7))
            
            # Get detailed column information
            cursor.execute(f'PRAGMA table_info("{table_name}")')
            columns = cursor.fetchall()
            
            for col in columns:
                cid, name, data_type, not_null, default_value, pk = col
                
                # Build column description
                col_desc = f"  {name} {data_type}"
                
                if pk:
                    col_desc += " PRIMARY KEY"
                if not_null and not pk:
                    col_desc += " NOT NULL"
                if default_value is not None:
                    col_desc += f" DEFAULT {default_value}"
                    
                lines.append(col_desc)
            
            # Get foreign key constraints
            cursor.execute(f'PRAGMA foreign_key_list("{table_name}")')
            foreign_keys = cursor.fetchall()
            
            if foreign_keys:
                lines.append("  FOREIGN KEYS:")
                for fk in foreign_keys:
                    id, seq, table, from_col, to_col, on_update, on_delete, match = fk
                    lines.append(f"    {from_col} -> {table}({to_col})")
            
            lines.append("")  # Empty line between tables
        
        conn.close()
        return '\n'.join(lines)
    
    except Exception as e:
        return f"Error retrieving structured schema: {e}"

def check_database_exists(db_path):
    """Check if database file exists and contains tables"""
    import os
    if not os.path.exists(db_path):
        return False, f"Database file '{db_path}' does not exist."
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        if not tables:
            return False, "Database file exists but contains no tables."
        
        return True, f"Database exists with {len(tables)} tables."
    
    except Exception as e:
        return False, f"Error checking database: {e}"

if __name__ == "__main__":
    # Check if database exists
    exists, message = check_database_exists(DB_PATH)
    print(f"Database check: {message}")
    
    if not exists:
        print("Creating sample database...")
        # Create the data directory if it doesn't exist
        import os
        # os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        # setup_sample_db()
    
    print("\nDETAILED SCHEMA:")
    print(get_structured_schema(DB_PATH))
    
    print("\nRAW SCHEMA:")
    print(get_db_schema(DB_PATH))