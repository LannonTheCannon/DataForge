# DataForge: AI-Powered Credit Card Fraud Analysis Platform 🛡️

DataForge is an advanced analytics platform that combines the power of AI and data visualization to provide comprehensive insights into credit card fraud patterns. Built with Streamlit and OpenAI, it offers an interactive interface for exploring and analyzing fraud detection data.

## 🚀 Features

### 1. Interactive Dashboard
- Real-time data visualization
- Key metrics and trends
- Customizable views and filters

### 2. AI-Powered Analysis
- OpenAI Integration for intelligent insights
- Natural language querying capabilities
- Advanced pattern recognition

### 3. Multi-Modal Analysis Tools
- **Story Telling**: Data-driven narrative exploration
- **Data Explorer**: In-depth data analysis interface
- **AI Chat**: Conversational interface for data queries
- **Pandas Chat**: Direct dataframe manipulation through chat

### 4. Smart Data Processing
- Automated data preparation
- Real-time data validation
- Intelligent summary generation

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **AI Integration**: OpenAI API
- **Data Processing**: Pandas, PandasAI
- **Visualization**: Streamlit native components
- **Data Storage**: Pickle serialization

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/DataForge.git

# Navigate to project directory
cd DataForge

# Install required packages
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY='your-api-key'

# Run the application
streamlit run main.py
```

## 🔧 Configuration

1. Set up your OpenAI API key in Streamlit secrets:
```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "your-api-key"
```

2. Configure Assistant ID and Thread ID:
```python
ASSISTANT_ID = 'your-assistant-id'
THREAD_ID = "your-thread-id"
```

## 📚 Usage

1. **Data Story**: Explore the narrative behind fraud patterns
2. **Dashboard**: View key metrics and visualizations
3. **Data Explorer**: Deep dive into raw data analysis
4. **AI Chat**: Ask questions about the dataset
5. **Pandas Chat**: Perform data manipulations via chat

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- Project Lead: [Your Name]
- AI Integration: [Team Member]
- Data Science: [Team Member]
- Frontend Development: [Team Member]

## 📞 Contact

For any queries, please reach out to [your-email@domain.com]
