# Healthcare SQL Analytics Enhancement

## Overview
This enhancement adds healthcare domain-specific intelligence to the SQL generation system, incorporating detailed schema notes and medical terminology understanding.

## Key Features

### 1. Healthcare Domain Context
- **Medical Terminology**: ICD-10, CPT, HCP, HCO, NPI, NDC, AWP, DAW codes
- **Healthcare Entities**: Providers, Patients, Claims, Procedures, Drugs, Therapy Areas
- **Industry Terms**: KOL (Key Opinion Leaders), Clinical Trials, Pharmaceutical Companies

### 2. Enhanced Agent Functions

#### `generate_sql(user_input, db_schema)`
- Healthcare-specialized SQL generation
- Incorporates schema notes for better column understanding
- Understands medical terminology and relationships

#### `review_sql(sql, db_schema)`
- Healthcare-specific query optimization
- Considers medical data patterns and performance
- Uses detailed schema notes for join optimization

#### `check_compliance(sql)`
- HIPAA and GDPR compliance checking
- PHI/PII exposure detection
- Healthcare-specific privacy requirements

#### `interpret_healthcare_query(user_input, db_schema)`
- **NEW**: Interprets healthcare business questions
- Identifies relevant tables and relationships
- Explains data requirements without generating SQL

#### `validate_healthcare_sql(sql, db_schema)`
- **NEW**: Validates queries against healthcare schema
- Checks table/column correctness
- Performance and best practices validation

### 3. Schema Notes Integration
- Loads detailed column descriptions from `SchemaNotes.txt`
- Includes sample data and column meanings
- Provides context for accurate query generation

### 4. Healthcare Data Tables
1. **as_lsf_v1**: Pharmaceutical payments to healthcare providers
2. **as_providers_v1**: Provider details and specialties
3. **as_providers_referrals_v2**: Referral patterns and relationships
4. **fct_pharmacy_clear_claim_allstatus_cluster_brand**: Pharmacy claims data
5. **mf_conditions**: Medical condition directory
6. **mf_providers**: KOL provider profiles
7. **mf_scores**: Provider performance scores

## Usage Examples

### Basic Healthcare Query
```python
from langchain_agents import generate_sql, interpret_healthcare_query
from utils.db_simulator import get_structured_schema, DB_PATH

# Load schema
db_schema = get_structured_schema(DB_PATH)

# Interpret query
interpretation = interpret_healthcare_query(
    "Find cardiologists with highest payment amounts", 
    db_schema
)

# Generate SQL
sql_result = generate_sql(
    "Show top 5 cardiologists by total payment amounts from pharma companies",
    db_schema
)
```

### Complete Healthcare Analytics Pipeline
```python
# 1. Interpret query
interpretation = interpret_healthcare_query(user_query, db_schema)

# 2. Generate SQL
sql_result = generate_sql(user_query, db_schema)

# 3. Review and optimize
reviewed_sql = review_sql(sql_result['text'], db_schema)

# 4. Validate query
validation = validate_healthcare_sql(reviewed_sql['text'], db_schema)

# 5. Check compliance
compliance = check_compliance(reviewed_sql['text'])

# 6. Execute if compliant
if "compliant" in compliance['text'].lower():
    result = run_query(reviewed_sql['text'])
```

## Sample Healthcare Queries

1. **Provider Analysis**
   - "Find all providers who received payments from ABBVIE for diabetes-related products"
   - "Show the top 5 KOL providers by score for cardiovascular conditions"

2. **Pharmacy Claims**
   - "List all pharmacy claims for patients with diabetes in 2023"
   - "Show the most prescribed drugs by total dispensed quantity"

3. **Referral Patterns**
   - "Find referral patterns between cardiologists and primary care physicians"
   - "Show providers with highest referral volumes by specialty"

4. **Payment Analysis**
   - "Show payment amounts by pharmaceutical company and therapeutic area"
   - "Find providers receiving payments for multiple therapy areas"

## Configuration

### Schema Notes File
Ensure `SchemaNotes.txt` is in the root directory with detailed column descriptions and sample data.

### Environment Variables
```bash
GEMINI_KEY=your_gemini_api_key
MODEL_NAME=gemini-2.5-flash
```

### Database Path
```python
DB_PATH = "dataset/data.sqlite"
```

## Testing

Run the test suite:
```bash
python test_healthcare_agents.py
```

Run the interactive main application:
```bash
python main.py
```

## Benefits

1. **Domain Expertise**: Understands healthcare terminology and relationships
2. **Better Accuracy**: Uses detailed schema notes for precise query generation
3. **Compliance**: Built-in healthcare privacy and compliance checking
4. **Validation**: Comprehensive query validation against healthcare schemas
5. **Interpretation**: Explains user queries in terms of available data

## Future Enhancements

- Integration with medical ontologies (SNOMED, UMLS)
- Real-time clinical decision support
- Advanced analytics for population health
- Integration with EHR systems
- Machine learning model integration for predictive analytics
