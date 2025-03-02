import streamlit as st
import sys
import os
from datetime import datetime
import pandas as pd
import json

# Import your workflow function
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from crew_workflow import get_summarized_news
from knowledge_graph import display_knowledge_graph

# Page configuration
st.set_page_config(
    page_title="AI Trend Tracker",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Basic CSS for styling
st.markdown("""
    <style>
    /* Main layout and typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    body {
        font-family: 'Inter', sans-serif;
        background-color: #f9fafb;
    }
    
    /* Header styles */
    .app-header {
        background: linear-gradient(90deg, #2c7be5 0%, #1d5abb 100%);
        color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    
    .app-subtitle {
        margin-top: 0.3rem;
        font-weight: 400;
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Card styles */
    .card {
        background-color: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.07);
        margin-bottom: 1rem;
        border: 1px solid #eaecef;
    }
    
    /* Article styles */
    .article-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1f36;
        margin-bottom: 0.5rem;
    }
    
    .article-meta {
        display: flex;
        align-items: center;
        margin-bottom: 0.8rem;
        font-size: 0.85rem;
        color: #5e6e82;
    }
    
    .source-badge {
        background-color: #EBF5FF;
        color: #2D7FF9;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-weight: 500;
        font-size: 0.75rem;
        margin-right: 0.75rem;
    }
    
    .article-summary {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #1a1f36;
        margin-bottom: 1rem;
        padding: 0.75rem;
        background-color: #f9fafb;
        border-radius: 6px;
    }
    
    /* Tag styles */
    .tags-container {
        display: flex;
        flex-wrap: wrap;
        margin-bottom: 0.75rem;
        gap: 0.5rem;
    }
    
    .tag {
        background-color: #EFF6FF;
        color: #2563EB;
        font-size: 0.75rem;
        padding: 0.25rem 0.6rem;
        border-radius: 16px;
    }
    
    .trend-tag {
        background-color: #DBEAFE;
        color: #1E40AF;
        font-size: 0.85rem;
        font-weight: 500;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        margin: 0.3rem;
    }
    
    .read-article-button {
        background-color: #ffffff;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.85rem;
        cursor: pointer;
        text-align: center;
        display: inline-block;
        transition: background-color 0.2s, transform 0.1s;
        text-decoration: none;
        margin-top: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
        
    .read-article-button:hover {
        background-color: #2876f9;
        text-decoration: none;
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .read-article-button:active {
        transform: translateY(1px);
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# App Header
st.markdown("""
    <div class="app-header">
        <div>
            <h1 class="app-title">🧠 AI Trend Tracker</h1>
            <p class="app-subtitle">Stay informed with the latest AI developments</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'news_data' not in st.session_state:
    st.session_state.news_data = None
    
if 'selected_sources' not in st.session_state:
    st.session_state.selected_sources = []

# Sidebar with simplified controls
with st.sidebar:
    st.header("Search & Filters")
    
    # Quick filters section
    st.subheader("Quick Filters")
    
    quick_filter = st.radio(
        "Topic",
        ["All AI News", "Generative AI", "AI Ethics", "Research Breakthroughs", "Business Applications"]
    )
    
    # Generate search terms based on selected quick filter
    if quick_filter == "All AI News":
        default_query = "Artificial Intelligence OR AI OR machine learning OR LLM"
    elif quick_filter == "Generative AI":
        default_query = "Generative AI OR LLM OR GPT OR diffusion model"
    elif quick_filter == "AI Ethics":
        default_query = "AI ethics OR AI bias OR AI regulation OR responsible AI"
    elif quick_filter == "Research Breakthroughs":
        default_query = "AI research breakthrough OR new AI model OR AI paper"
    else:  # Business Applications
        default_query = "AI business application OR enterprise AI OR AI startup"
    
    # Search options    
    st.subheader("Search Terms")
    query = st.text_area(
        "Custom search query",
        value=default_query,
        height=80
    )
    
    col1, col2 = st.columns(2)
    with col1:
        days = st.slider(
            "Days",
            min_value=1,
            max_value=30,
            value=7
        )
    
    with col2:
        article_count = st.slider(
            "Articles",
            min_value=5,
            max_value=30,
            value=10
        )
    
    # Display options
    st.subheader("Display Options")
    min_importance = st.slider("Minimum Importance", 1, 10, 1)
    
    # Fetch button
    fetch_pressed = st.button("🔄 Refresh News", type="primary", use_container_width=True)
    
    if st.button("🗑️ Clear Cache", use_container_width=True):
        st.session_state.news_data = None
        st.toast("Cache cleared successfully!")
    
    # About section
    with st.expander("About This App"):
        st.markdown("""
        This application uses AI to analyze the latest news in artificial intelligence:
        
        1. **Finding** relevant AI news articles
        2. **Summarizing** content to key points
        3. **Rating** articles by importance
        4. **Identifying** emerging trends
        
        Built with Streamlit and OpenAI.
        """)

# Fetch data if button is pressed or if there's nothing in session state yet
if fetch_pressed or st.session_state.news_data is None:
    with st.spinner("Gathering the latest AI insights..."):
        try:
            st.session_state.news_data = get_summarized_news(
                query_terms=query,
                days=days,
                article_count=article_count,
                preferred_sources=None
            )
            st.session_state.selected_sources = []
            st.success("Successfully retrieved AI news!")
        except Exception as e:
            st.error(f"Error retrieving news: {str(e)}")
            if st.session_state.news_data is None:
                st.session_state.news_data = {"articles": [], "trends": {}, "error": str(e)}

# Content area
if st.session_state.news_data:
    news_data = st.session_state.news_data
    articles = news_data.get("articles", [])
    trends = news_data.get("trends", {})
    
    # Error handling
    if "error" in news_data and news_data["error"]:
        st.error(f"Error fetching news: {news_data['error']}")
        st.info("Try adjusting your search terms or time range.")
    
    # Collect all unique sources
    all_sources = set()
    
    for article in articles:
        s_name = article.get("source", {}).get("name", "").strip()
        if s_name:
            all_sources.add(s_name)
    
    all_sources = sorted(list(all_sources))
    
    # Overview metrics
    st.header("📊 Overview")
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("Articles Found", len(articles))
    
    with cols[1]:
        trending_topics = trends.get("trending_topics", [])
        st.metric("Trending Topics", len(trending_topics))
    
    with cols[2]:
        avg_importance = trends.get('average_importance', 0)
        st.metric("Average Importance", f"{avg_importance:.1f}/10")
    
    with cols[3]:
        st.metric("Days Searched", days)
    
    # Trending Topics section
    st.header("🔥 Trending Topics")
    
    if trending_topics:
        # Create a tag cloud
        st.markdown("<div style='text-align:center;padding:1rem;'>", unsafe_allow_html=True)
        for topic in trending_topics:
            st.markdown(f"<span class='trend-tag'>{topic}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No trending topics identified from the current articles.")
        
    # Combined summary section
    st.header("📝 Executive Summary")
    combined_summary = news_data.get("combined_summary", "")
    if combined_summary:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #3a86ff; margin-bottom: 2rem;">
            <p style="font-size: 1.05rem; line-height: 1.6; color: #333; font-style: normal;">
        """ + combined_summary.replace("\n", "<br>") + """
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No executive summary available. Try refreshing the news.")
    
    # Source filtering
    if all_sources:
        st.header("🔍 Filter by Source")
        
        # Source checkboxes
        cols = st.columns(3)
        sources_per_col = len(all_sources) // 3 + 1
        
        col_idx = 0
        for i, source in enumerate(all_sources):
            if i > 0 and i % sources_per_col == 0:
                col_idx += 1
            
            with cols[min(col_idx, 2)]:
                is_selected = source in st.session_state.selected_sources
                if st.checkbox(source, value=is_selected, key=f"source_{i}"):
                    if source not in st.session_state.selected_sources:
                        st.session_state.selected_sources.append(source)
                else:
                    if source in st.session_state.selected_sources:
                        st.session_state.selected_sources.remove(source)
    
    # Filter the articles
    filtered_articles = articles
    
    # Apply source filter if needed
    if st.session_state.selected_sources:
        filtered_articles = [
            art for art in filtered_articles
            if art.get("source", {}).get("name") in st.session_state.selected_sources
        ]
    
    # Filter by minimum importance score
    filtered_articles = [
        art for art in filtered_articles
        if art.get("importance_score", 0) >= min_importance
    ]
    
    # Main articles section
    st.header("📰 Latest AI News")
    
    if filtered_articles:
        # Sort articles by importance score (highest first)
        filtered_articles.sort(key=lambda x: x.get("importance_score", 0), reverse=True)
        
        # Articles view
        for article in filtered_articles:
            importance = article.get("importance_score", 0)
            
            # Format the date
            published_date = article.get('publishedAt', '')
            try:
                if published_date:
                    parsed_date = datetime.strptime(published_date.split('T')[0], '%Y-%m-%d')
                    formatted_date = parsed_date.strftime('%b %d, %Y')
                else:
                    formatted_date = "Unknown Date"
            except Exception:
                formatted_date = published_date
            
            # Article card
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            # Title and metadata
            st.markdown(f"""
            <div class="article-title">{article.get('title', 'Untitled')}</div>
            <div class="article-meta">
                <span class="source-badge">{article.get('source', {}).get('name', 'Unknown')}</span>
                <span>📅 {formatted_date}</span>
                <span style="margin-left: auto;">Importance: {importance}/10</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Display article summary
            st.markdown(f'<div class="article-summary">{article.get("summary", "No summary available")}</div>', unsafe_allow_html=True)
            
            # Key points as tags
            key_points = article.get("key_points", [])
            if key_points:
                st.markdown('<div class="tags-container">', unsafe_allow_html=True)
                for point in key_points:
                    if isinstance(point, str) and point.strip():
                        st.markdown(f'<span class="tag">{point.strip()}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Link to full article
            url = article.get("url", "")
            if url:
                st.markdown(f'''
                    <a href="{url}" target="_blank" class="read-article-button">
                        <span style="margin-right: 5px;">📄</span> Read Full Article
                    </a>''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        if st.session_state.selected_sources:
            st.warning("No articles match your selected sources. Try adjusting your filters.")
        else:
            st.warning("No articles found matching your search criteria. Try broadening your search terms.")

    # Knowledge Graph section
    if articles:  # Use the main articles list, not filtered_articles
        # Display the knowledge graph with all articles for better connections
        display_knowledge_graph(articles, trends)
    else:
        st.info("No articles available for knowledge graph visualization. Try refreshing the news.")

# Footer
st.markdown(f"""
    <div style="text-align:center; margin-top:2rem; font-size:0.8rem; color:#666;">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
""", unsafe_allow_html=True)