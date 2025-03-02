# AI Trend Tracker

A Streamlit-based web application that tracks, summarizes, and analyzes the latest developments in artificial intelligence using CrewAI and OpenAI.

## 🧠 Features

- **AI News Aggregation**: Collects the latest AI news from reputable sources
- **Intelligent Summarization**: Automatically summarizes articles and rates their importance
- **Trend Analysis**: Identifies and visualizes emerging trends in AI
- **Executive Summaries**: Generates comprehensive overviews of the current AI landscape
- **Customizable Searches**: Filter by topic, time range, and source

## 🛠️ Technologies

- **Streamlit**: For the web application interface
- **CrewAI**: For agent-based workflow orchestration
- **OpenAI**: For intelligent content analysis and summarization
- **Python**: Core programming language

## 📊 How It Works

AI Trend Tracker uses a multi-agent system powered by CrewAI to process news articles:

1. **News Extractor Agent**: Fetches relevant AI news articles based on search parameters
2. **News Summarizer Agent**: Analyzes and summarizes each article, assigning importance scores
3. **Trend Analyzer Agent**: Identifies patterns and emerging trends across articles
4. **Executive Summarizer Agent**: Creates a comprehensive overview of the current AI landscape

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key
- Perigon API key (for news retrieval)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/ai-trend-tracker.git
   cd ai-trend-tracker
   ```

4. Setup the virtual inviroment
   ```bash
   The guide can be found in setup.md
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your configuration
   - Create a `config.py` file with the following content:
   ```python
   # Configuration file for API keys and other settings
   OPENAI_API_KEY = "your-openai-api-key-here"
   PERIGON_API_KEY = "your-perigon-api-key-here"
   ```

5. Run the application
   ```bash
   streamlit run app.py
   ```

## 🧩 Project Structure

```
AI-TREND-TRACKER/
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration settings
├── agents.py                 # Agent definitions and tools
├── crew_workflow.py          # CrewAI workflow implementation
├── knowledge_graph.py        # Knowledge graph visualization
├── requirements.txt          # Project dependencies
├── README.md                 # Main project documentation
├── documantation.md          # Assignment implementation details
└── setup.md                  # Virtual environment setup guide
```

## 🔍 Usage

1. **Choose a Topic**: Select a pre-defined filter or create a custom search query
2. **Set Parameters**: Adjust the time range and number of articles
3. **Refresh News**: Click the refresh button to fetch the latest articles
4. **Explore Results**: Browse through trending topics, executive summary, and article details
5. **Filter**: Use the source filter to narrow down results by publication

## 🔄 CrewAI Implementation

The application offers two modes of operation:

1. **Full CrewAI Mode**: Uses the complete agent-based workflow with CrewAI for maximum flexibility and agent interaction
2. **Simplified Pipeline**: Uses a direct function-based approach for faster results

## Additional Documentation

For more detailed information about the project:
- [Assignment ansswering](documantation.md): Details about the design and implementation in relation to the academic assignment
- [Virtual Environment Setup](setup.md): Detailed guide for setting up the virtual environment

## Contributors

- Vittorio Wollner Infante Papa
- Oliver Højbjerre-Frandsen
- Daniel Sørensen Riisager
