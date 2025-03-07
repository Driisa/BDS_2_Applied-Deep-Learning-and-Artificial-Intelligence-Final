from crewai import Crew, Process, Task
from agents import (
    NewsExtractorTools, NewsSummarizerTools, NewsTrendAnalyzerTools, CombinedSummaryTools,
    news_extractor_agent, news_summarizer_agent, trend_analyzer_agent, executive_summarizer_agent
)

def filter_by_sources(articles, preferred_sources):
    """Filter articles based on source."""
    if not preferred_sources:
        return articles
        
    return [
        article for article in articles
        if article.get("source", {}).get("name") in preferred_sources
    ]

def get_summarized_news(query_terms=None, days=7, article_count=10, preferred_sources=None):
    """Run the full pipeline using CrewAI: extract, summarize, and analyze AI news."""
    try:
        # Initialize tools
        extractor_tools = NewsExtractorTools()
        summarizer_tools = NewsSummarizerTools()
        trend_tools = NewsTrendAnalyzerTools()
        summary_tools = CombinedSummaryTools()
        
        # Create tasks
        fetch_task = Task(
            description=f"""
                Fetch the latest AI news articles using the following parameters:
                - Search terms: {query_terms or 'AI, Artificial Intelligence, Machine Learning, LLM'}
                - Days ago: {days}
                - Number of articles: {article_count}
                
                Return a list of normalized article objects with title, url, description, content, source, and publishedAt fields.
            """,
            agent=news_extractor_agent,
            expected_output="A list of news article objects",
            output_file="latest_ai_news.json"
        )
        
        summarize_task = Task(
            description="""
                Analyze and summarize each article in the provided list.
                For each article:
                1. Create a concise 3-5 sentence summary
                2. Rate its importance on a scale of 1-10
                3. Extract 3 key points
                
                Return a list of enriched article objects with summary, importance_score, and key_points fields.
            """,
            agent=news_summarizer_agent,
            expected_output="A list of summarized article objects",
            output_file="summarized_ai_news.json",
            context=[fetch_task]
        )
        
        analyze_trends_task = Task(
            description="""
                Analyze the summarized articles to identify emerging trends and patterns.
                
                Extract:
                1. Top trending topics
                2. Top articles by importance
                3. Average importance score
                
                Return a structured object with trending_topics, top_articles, and average_importance fields.
            """,
            agent=trend_analyzer_agent,
            expected_output="An analysis object with trending topics and patterns",
            output_file="ai_trend_analysis.json",
            context=[summarize_task]
        )
        
        create_executive_summary_task = Task(
            description="""
                Create a comprehensive executive summary of the AI landscape based on the analyzed articles.
                
                The summary should:
                1. Provide a high-level overview of current AI developments
                2. Focus on the most important articles by importance score
                3. Group related technologies and highlight significant breakthroughs
                4. End with insights about the near future of AI
                
                Format as a cohesive 3-4 paragraph summary without bullet points or numbered lists.
            """,
            agent=executive_summarizer_agent,
            expected_output="A cohesive executive summary as a string",
            output_file="ai_executive_summary.txt",
            context=[summarize_task, analyze_trends_task]
        )
        
        # Create the crew
        ai_news_crew = Crew(
            agents=[news_extractor_agent, news_summarizer_agent, trend_analyzer_agent, executive_summarizer_agent],
            tasks=[fetch_task, summarize_task, analyze_trends_task, create_executive_summary_task],
            verbose=True,  # Changed from 2 to True
            process=Process.sequential
        )
        
        # Alternative simpler implementation that doesn't require running the full crew
        def run_simplified_pipeline():
            # Step 1: Fetch news articles
            latest_news = extractor_tools.fetch_latest_ai_news(query_terms, days, article_count)
            
            if preferred_sources:
                latest_news = filter_by_sources(latest_news, preferred_sources)
            
            if not latest_news:
                return {
                    "articles": [],
                    "trends": {},
                    "error": "No articles found matching the criteria."
                }

            # Step 2: Summarize articles
            summarized_news = summarizer_tools.batch_summarize_articles(latest_news)
            
            # Step 3: Sort articles by importance
            summarized_news.sort(key=lambda x: x.get("importance_score", 0), reverse=True)
            
            # Step 4: Extract trends
            trends = trend_tools.analyze_trends(summarized_news)
            
            # Step 5: Generate a combined summary
            combined_summary = summary_tools.generate_combined_summary(summarized_news)
            
            return {
                "articles": summarized_news,
                "trends": trends,
                "combined_summary": combined_summary,
                "total_articles": len(summarized_news),
                "query_parameters": {
                    "days": days,
                    "article_count": article_count,
                    "preferred_sources": preferred_sources or "All"
                }
            }
        
        # Choose which implementation to use (True: full CrewAI implementation or False: simplified pipeline)
        USE_FULL_CREW = False
        
        if USE_FULL_CREW:
            result = ai_news_crew.kickoff()
            
            # Process and format the results
            return {
                "articles": [],  
                "trends": {},    
                "combined_summary": "",  
                "error": "Full CrewAI implementation not fully implemented yet."
            }
        else:
            # Run the simplified pipeline
            return run_simplified_pipeline()
            
    except Exception as e:
        print(f"Error in news processing workflow: {str(e)}")
        return {
            "articles": [],
            "trends": {},
            "error": str(e)
        }