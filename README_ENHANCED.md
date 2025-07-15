# 🏥 Healthcare SQL Analytics Platform

A professional, AI-powered healthcare data analytics platform built with Streamlit and LangChain. This application provides natural language querying capabilities for healthcare databases with built-in compliance checking and domain expertise.

## ✨ Key Features

### 🎯 Enhanced User Interface
- **Professional Healthcare Theme**: Clean, modern design with medical color scheme
- **Interactive Query Builder**: Step-by-step query construction with visual feedback
- **Real-time Progress Tracking**: Visual indicators for each processing step
- **Example Query Gallery**: Pre-built queries for common healthcare analytics

### 🧠 AI-Powered Analytics
- **Natural Language Processing**: Convert plain English to SQL queries
- **Healthcare Domain Intelligence**: Understanding of medical terminology and relationships
- **Multi-Agent Pipeline**: Generate → Review → Validate → Execute workflow
- **Compliance Checking**: HIPAA/GDPR compliance validation

### 📊 Advanced Analytics
- **Query Interpretation**: Explains what data you're looking for
- **SQL Optimization**: Automatic query review and performance improvements
- **Result Visualization**: Enhanced display of query results
- **Cost Tracking**: Monitor AI usage costs in real-time

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- SQLite database with healthcare data
- Google Gemini API key

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SQLRx-DocSearchAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements-enhanced.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GEMINI_KEY=your_api_key_here" > .env
   ```

4. **Launch the application**
   ```bash
   python launch_app.py
   ```
   
   Or run directly:
   ```bash
   streamlit run app.py
   ```

## 📋 Application Overview

### Main Interface Components

#### 1. 🎯 Query Input Area
- **Natural Language Input**: Large text area for entering healthcare queries
- **Example Integration**: Click examples to auto-populate query field
- **Smart Suggestions**: Context-aware query completion

#### 2. 📊 Analytics Dashboard
- **Cost Tracking**: Real-time monitoring of AI API usage
- **Progress Indicators**: Visual feedback for each processing step
- **Performance Metrics**: Query execution statistics

#### 3. 🔍 Processing Pipeline
1. **Query Interpretation**: Understand what data you're looking for
2. **SQL Generation**: Create optimized SQL queries
3. **Review & Validation**: Check query correctness and performance
4. **Compliance Check**: Ensure HIPAA/GDPR compliance
5. **Execution**: Run approved queries safely

#### 4. 📚 Help & Documentation
- **Healthcare Terms**: Comprehensive glossary of medical terminology
- **Data Tables**: Information about available datasets
- **Query Tips**: Best practices for effective queries

### Enhanced Features

#### 🏥 Healthcare Domain Intelligence
- **Medical Terminology**: Understands ICD-10, CPT, NPI, NDC codes
- **Provider Networks**: Analyzes relationships between healthcare professionals
- **Pharmaceutical Data**: Processes payment and prescription information
- **Compliance Focus**: Built-in privacy and regulatory compliance

#### 🎨 Professional UI/UX
- **Modern Design**: Clean, professional healthcare-themed interface
- **Responsive Layout**: Works on desktop and tablet devices
- **Interactive Elements**: Hover effects, smooth transitions
- **Visual Hierarchy**: Clear organization of information

## 💾 Database Schema

The application works with healthcare databases containing:

### Core Tables
- **as_lsf_payments**: Pharmaceutical payments to providers
- **as_providers**: Healthcare provider information
- **mf_providers**: Key Opinion Leader profiles
- **as_providers_referrals**: Provider referral patterns
- **fct_pharmacy_claims**: Prescription claims data
- **mf_conditions**: Medical condition directory
- **mf_scores**: Provider performance metrics

## 🔧 Configuration

### Streamlit Configuration
The app includes custom configuration in `.streamlit/config.toml`:
- Healthcare-themed color scheme
- Optimized server settings
- Professional styling

### Environment Variables
```bash
GEMINI_KEY=your_google_gemini_api_key
MODEL_NAME=gemini-2.5-flash
```

## 📖 Usage Examples

### Example Queries
- "Show me the top 10 providers by total payment amounts"
- "Find all cardiologists who received payments from pharmaceutical companies"
- "What are the most prescribed medications for diabetes?"
- "Analyze referral patterns between specialists and primary care"

### Step-by-Step Workflow
1. **Enter Query**: Type your healthcare question in natural language
2. **Interpret**: Click "Analyze Query" to understand data requirements
3. **Generate**: Click "Generate SQL" to create the database query
4. **Review**: System automatically reviews and optimizes the query
5. **Validate**: Comprehensive validation against healthcare schema
6. **Check Compliance**: Ensure HIPAA/GDPR compliance
7. **Execute**: Run the approved query and view results

## 🔒 Security & Compliance

### Data Protection
- **HIPAA Compliance**: Automatic checking for protected health information
- **GDPR Compliance**: Privacy regulation adherence
- **Access Controls**: Session-based security measures
- **Audit Trail**: Comprehensive logging of all queries

### Best Practices
- No direct patient identifiers in queries
- Aggregated data analysis focus
- Secure API key management
- Regular compliance monitoring

## 🚀 Advanced Features

### Query Optimization
- **Performance Analysis**: Automatic query optimization
- **Index Recommendations**: Suggestions for database improvements
- **Cost Estimation**: Predict query execution costs

### Analytics Dashboard
- **Real-time Metrics**: Live monitoring of application performance
- **Usage Statistics**: Track query patterns and costs
- **Efficiency Scoring**: Measure query effectiveness

## 🛠️ Development

### Project Structure
```
├── app.py                 # Main Streamlit application
├── langchain_agents.py    # AI agent implementations
├── utils/
│   ├── db_simulator.py    # Database utilities
│   ├── helper.py          # Helper functions
│   └── ui_helpers.py      # UI utility functions
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── requirements-enhanced.txt
└── launch_app.py          # Application launcher
```

### Testing
```bash
# Run the test suite
python test_healthcare_agents.py

# Run specific functionality tests
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check the documentation
- Review example queries

## 🏆 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://langchain.com/)
- AI models by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Healthcare data standards by [CMS](https://www.cms.gov/)

---

**🏥 Healthcare SQL Analytics Platform** - Making healthcare data analysis accessible, compliant, and professional.
