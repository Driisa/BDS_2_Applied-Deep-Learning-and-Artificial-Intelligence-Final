# 📝 AI Trend Tracker: Assignment Implementation Details

## 📋 Assignment Objectives

The assignment required the development of an innovative project that:
- Employs GPT models and AI agents to address a real-world problem
- Implements prompt engineering techniques
- Develops an interactive Streamlit application
- Includes a knowledge graph visualization (Optionally)

## 🎯 Problem Addressed

AI Trend Tracker addresses the real-world challenge of **information overload in AI research and development**. The field of AI moves rapidly, with a lot of developments published often across various platforms. This creates a significant challenge for professionals, researchers, and enthusiasts to stay informed about the all the latest trends, breakthroughs, and applications.

The solution is a automated process:
1. Finding relevant AI news from reliable sources
2. Determining which developments are truly significant
3. Extracting key points and emerging trends
4. Presenting the information in an accessible, organized format

## 🧩 Agent Architecture

The application implements a CrewAI-based multi-agent system with four specialized agents:

### 1. News Extractor Agent
- **Role**: AI News Extractor
- **Goal**: Retrieve the latest AI news from reputable sources
- **Backstory**: Expert AI journalist with years of experience tracking AI industry trends
- **Implementation**: Uses the Perigon API to retrieve recent AI-related news articles based on customizable search parameters

### 2. News Summarizer Agent
- **Role**: AI News Analyzer and Summarizer
- **Goal**: Create insightful summaries of AI news that highlight true significance and filter hype
- **Backstory**: Distinguished AI researcher with expertise in contextualizing new developments
- **Implementation**: Uses OpenAI's GPT models to analyze articles and produce summaries, importance ratings, and key points

### 3. Trend Analyzer Agent
- **Role**: AI Trend Analyst
- **Goal**: Identify emerging patterns and significant developments in AI technology
- **Backstory**: Experienced technology trend analyst specializing in artificial intelligence
- **Implementation**: Processes article metadata and content to identify recurring themes and topics

### 4. Executive Summarizer Agent
- **Role**: Executive AI Insights Specialist
- **Goal**: Create comprehensive overviews of AI developments for busy professionals
- **Backstory**: Former technology executive turned AI researcher
- **Implementation**: Synthesizes information across all articles to produce a coherent executive summary

## 🔍 Prompt Engineering Techniques

The project demonstrates prompt engineering through:

### Structured Templates
```python
self.prompt_template = """
Analyze this AI news article and provide:
1. A concise 5-9 sentence summary highlighting key innovations and significance
2. An importance rating (1-10)
3. Three specific key points as a comma-separated list

Article to summarize:
Title: {title}
Description: {description}
Content: {content}

Format your response as:
SUMMARY: [insightful summary]
IMPORTANCE: [1-10 score]
KEY_POINTS: [comma-separated list of 3 specific key points]
"""
```

### Role and System Messages
```python
response = self.client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are an AI technology analyst who can identify significant developments and summarize them concisely."
        },
        {
            "role": "user",
            "content": final_prompt
        }
    ],
    temperature=0.3 #this is how creative the model is allow to be
)
```

### Contextual Executive Summary Prompting
The executive summary generation uses prompting that:
- Provides the most important articles
- Includes trending topics to guide theme identification
- Gives explicit formatting instructions
- Specifies the desired level of technical language

## 🌐 Knowledge Graph Implementation

The optional knowledge graph component:

- **Visualizes relationships** between trending topics, articles, and key points
- **Color-codes different entity types** for clarity (blue for topics, pink for articles, purple for key points)
- **Sizes nodes** based on importance and centrality
- **Weights connections** to show strength of relationships

The implementation uses NetworkX for the graph and PyVis for visualization, enabling users to:
- Click and drag nodes to rearrange the graph
- Zoom in/out with mouse wheel
- Hover over nodes to see full titles
- Click on a node to focus on its connections

## 💻 Streamlit Application

The Streamlit application provides:

- **Interactive Controls**: Custom search parameters, time range adjustment, and filtering options
- **Visual Data Presentation**: Trend tags, importance metrics, and summary cards
- **Dynamic Filtering**: Source and importance-based filtering of results
- **Responsive Design**: Clean, intuitive interface with proper visual hierarchy

## 📊 Results and Impact

The AI Trend Tracker agentic application demonstrates how AI agents can:
1. Process and analyze information efficiently
2. Extract meaningful patterns and insights
3. Present complex information in accessible formats
4. Save users significant time in staying informed about AI developments

## 🔄 CrewAI Implementation

The project offers two implementation approaches:

1. **Full CrewAI Mode**: Uses the complete agent-based workflow for maximum flexibility
2. **Simplified Pipeline**: Uses a direct function-based approach for faster results

---

*This project was developed as part of the Final Assignment for the Agentic Systems course at Aalborg University.*
