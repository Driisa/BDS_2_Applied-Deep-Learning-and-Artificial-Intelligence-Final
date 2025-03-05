import streamlit as st
import networkx as nx
from pyvis.network import Network
import re
import streamlit.components.v1 as components
from typing import List, Dict, Any

def clean_text(text):
    """Clean topic text by removing special characters and converting to lowercase."""
    if not isinstance(text, str):
        return ""
    return re.sub(r'[^\w\s]', '', text.lower())

def build_knowledge_graph(articles: List[Dict[Any, Any]], trends: Dict[Any, Any]):
    """Build a knowledge graph from articles and detected trends."""
    # Initialize graph
    G = nx.Graph()
    
    # Extract trending topics and add as central nodes
    trending_topics = trends.get("trending_topics", [])
    
    # Add trending topics as main nodes
    for topic in trending_topics:
        clean_topic = clean_text(topic)
        if clean_topic:
            G.add_node(clean_topic, size=20, group=1, title=topic, label=topic)
    
    # Process articles
    for article in articles:
        # Get article properties
        title = article.get("title", "Untitled")
        source = article.get("source", {}).get("name", "Unknown")
        importance = article.get("importance_score", 0)
        key_points = article.get("key_points", [])
        
        # Clean key points
        clean_points = [clean_text(point) for point in key_points if isinstance(point, str)]
        clean_points = [point for point in clean_points if point]
        
        # Add article as a node
        short_title = title[:30] + "..." if len(title) > 30 else title
        article_node = f"article_{short_title}"
        G.add_node(article_node, size=10, group=2, title=title, label=short_title)
        
        # Connect article to related trending topics
        for topic in trending_topics:
            topic_clean = clean_text(topic)
            if not topic_clean:
                continue
                
            # Check if article title or key points contain the topic
            title_clean = clean_text(title)
            if topic_clean in title_clean or any(topic_clean in point for point in clean_points):
                G.add_edge(article_node, topic_clean, weight=importance/2)
        
        # Connect key points to the article
        for point in clean_points:
            if len(point) > 5:  
                point_node = f"point_{point[:20]}" 
                G.add_node(point_node, size=5, group=3, title=point, label=point[:20] + "...")
                G.add_edge(article_node, point_node, weight=1)
                
                # Connect key points to related trending topics
                for topic in trending_topics:
                    topic_clean = clean_text(topic)
                    if topic_clean and topic_clean in point:
                        G.add_edge(point_node, topic_clean, weight=1)
    
    return G

def generate_interactive_graph(G, height=500):
    """Generate an interactive HTML visualization of the knowledge graph."""
    # Create pyvis network
    net = Network(height=f"{height}px", width="100%", bgcolor="#ffffff", font_color="#333333")
    
    # Configure physics
    net.barnes_hut(gravity=-5000, central_gravity=0.3, spring_length=150, spring_strength=0.05)
    
    # Add nodes with properties
    for node, attrs in G.nodes(data=True):
        size = attrs.get('size', 10)
        group = attrs.get('group', 0)
        title = attrs.get('title', node)
        label = attrs.get('label', node)
        
        # Set node color based on group
        if group == 1:  # Trending topics
            color = "#3a86ff"  # Blue for trending topics
        elif group == 2:  # Articles
            color = "#ff006e"  # Pink for articles
        else:  # Key points
            color = "#8338ec"  # Purple for key points
            
        net.add_node(node, size=size, color=color, title=title, label=label)
    
    # Add edges with properties
    for source, target, attrs in G.edges(data=True):
        weight = attrs.get('weight', 1)
        net.add_edge(source, target, value=weight)
    
    # Generate HTML
    try:
        path = "knowledge_graph.html"
        net.save_graph(path)
        
        # Read the HTML file
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
            
        return html
    except Exception as e:
        print(f"Error generating graph: {str(e)}")
        return None

def display_knowledge_graph(articles, trends):
    """Display a knowledge graph visualization in Streamlit."""
    st.header("🔍 AI Trends Knowledge Graph")
    
    # Instructions
    with st.expander("ℹ️ How to use the knowledge graph"):
        st.markdown("""
        This knowledge graph visualizes connections between trending AI topics, articles, and key points:
        
        - **Blue nodes**: Trending topics in AI
        - **Pink nodes**: News articles
        - **Purple nodes**: Key points from articles
        
        **Tips for interaction**:
        - Click and drag nodes to rearrange the graph
        - Zoom in/out with mouse wheel
        - Hover over nodes to see full titles
        - Click on a node to focus on its connections
        
        The size of connections indicates the importance of the relationship.
        """)
    
    # Build the graph
    with st.spinner("Generating knowledge graph..."):
        G = build_knowledge_graph(articles, trends)
        
        if G.number_of_nodes() == 0:
            st.warning("Not enough data to generate a knowledge graph. Try adjusting your search parameters.")
            return
        
        # Generate and display the interactive graph
        html = generate_interactive_graph(G, height=600)
        if html:
            components.html(html, height=650)
        else:
            st.error("Failed to generate the knowledge graph. Please try again.")
    
    # Graph insights
    st.subheader("Graph Insights")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Topics", len([n for n, attrs in G.nodes(data=True) if attrs.get('group') == 1]))
    with col2:
        st.metric("Articles", len([n for n, attrs in G.nodes(data=True) if attrs.get('group') == 2]))
    with col3:
        st.metric("Connections", G.number_of_edges())