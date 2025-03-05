# AI Trend Tracker

A Streamlit-based web application that tracks, summarizes, and analyzes the latest developments in artificial intelligence using CrewAI and OpenAI.

## 🧠 Features

- **AI News Aggregation**: Collects the latest AI news from reputable sources via the Perigon API
- **Intelligent Summarization**: Automatically summarizes articles and rates their importance on a 1-10 scale
- **Trend Analysis**: Identifies and visualizes emerging trends in AI across multiple sources
- **Executive Summaries**: Generates comprehensive overviews of the current AI landscape
- **Knowledge Graph**: Visualizes connections between topics, articles, and key points
- **Customizable Searches**: Filter by topic, time range, source, and importance score

## 🛠️ Technologies

- **Streamlit**: For the web application interface
- **CrewAI**: For agent-based workflow orchestration
- **OpenAI**: For intelligent content analysis and summarization
- **BeautifulSoup**: For web scraping and content extraction
- **NetworkX & PyVis**: For knowledge graph creation and visualization
- **Pandas**: For data handling and manipulation

## 📊 How It Works

AI Trend Tracker uses a multi-agent system powered by CrewAI to process news articles:

1. **News Extractor Agent**: Fetches relevant AI news articles using the Perigon API and extracts full content from URLs
2. **News Summarizer Agent**: Analyzes each article to produce concise summaries, importance scores, and key points
3. **Trend Analyzer Agent**: Identifies patterns and emerging trends by analyzing topics across all articles
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

2. Setup the virtual environment
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
├── documentation.md          # Implementation details
├── setup.md                  # Virtual environment setup guide
└── Previous Searches/        # Directory for saved search results
```

## 🔍 Usage

1. **Choose a Topic**: Select a pre-defined filter (All AI News, Generative AI, AI Ethics, Research Breakthroughs, Business Applications) or create a custom search query
2. **Set Parameters**: Adjust the time range (1-30 days) and number of articles (5-30)
3. **Refresh News**: Click the refresh button to fetch the latest articles
4. **Explore Results**: 
   - View trending topics identified across articles
   - Read the executive summary of key developments
   - Browse through article cards with summaries and key points
   - Explore the knowledge graph visualization
5. **Filter Results**:
   - Filter by source publication
   - Set minimum importance score threshold
   - Clear cache to reset all data

## 🔄 Implementation Approaches

The application offers two modes of operation:

1. **Full CrewAI Mode**: Uses the complete agent-based workflow with CrewAI for maximum flexibility and agent interaction
2. **Simplified Pipeline Mode**: Uses a direct function-based approach for faster results (currently the default)

You can toggle between these modes by changing the `USE_FULL_CREW` flag in `crew_workflow.py`.

## 💾 Data Storage

The application stores data in several ways:

1. **Session State**: Temporary storage during user interaction
2. **JSON Files**: Search results are saved in the "Previous Searches" directory with date and query information
3. **Task Output Files**: The CrewAI workflow can save intermediate results to JSON and text files

## Additional Documentation

For more detailed information about the project:
- [Implementation Details](documentation.md): Technical details about the system design and implementation
- [Virtual Environment Setup](setup.md): Detailed guide for setting up the virtual environment

## Contributors

- Vittorio Wollner Infante Papa
- Oliver Højbjerre-Frandsen
- Daniel Sørensen Riisager