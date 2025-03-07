from crewai import Agent
from openai import OpenAI
from datetime import datetime, timedelta
import requests
from typing import List, Dict, Any
import config
import os
import json
from bs4 import BeautifulSoup

class NewsExtractorTools:
    def extract_content_from_url(self, url: str) -> str:
        """Extract article content from a given URL using BeautifulSoup."""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove script and style elements
                for element in soup(['script', 'style']):
                    element.decompose()
                
                # Get text content
                text = soup.get_text(separator='\n', strip=True)
                
                # Clean up the text
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                content = '\n'.join(lines)
                
                return content
            return ""
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return ""

    def fetch_latest_ai_news(self, query_terms=None, days=7, article_count=10, save_results=False):
        """Fetch AI-related news from Perigon API."""
        try:
            query = query_terms or "Artificial Intelligence OR AI OR machine learning OR LLM"
            
            end_date = datetime.today().strftime('%Y-%m-%d')  
            start_date = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')

            url = "https://api.goperigon.com/v1/all"
            params = {
                "apiKey": config.PERIGON_API_KEY,
                "q": query,
                "from": start_date,
                "to": end_date,
                "sortBy": "relevance",
                "language": "en",
                "size": article_count
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                
                normalized_articles = []
                for article in articles:
                    article_url = article.get("url", "")
                    # Extract content from URL if available
                    extracted_content = self.extract_content_from_url(article_url) if article_url else ""
                    
                    normalized_article = {
                        "title": article.get("title", "Untitled"),
                        "url": article_url,
                        "publishedAt": article.get("pubDate", article.get("publishedAt", "")),
                        "description": article.get("description", ""),
                        "content": extracted_content or article.get("content", ""),
                        "source": {
                            "name": article.get("source", {}).get("domain", 
                                    article.get("source", {}).get("name", "Unknown Source"))
                        }
                    }
                    normalized_articles.append(normalized_article)

                # Save results to JSON file if save_results is True
                if save_results and normalized_articles:
                    # Create Previous Searches directory if it doesn't exist
                    save_dir = os.path.join(os.path.dirname(__file__), "Previous Searches")
                    os.makedirs(save_dir, exist_ok=True)
                    
                    # Create filename with date and query terms
                    search_date = datetime.now().strftime("%Y-%m-%d")
                    query_part = query_terms[:30] if query_terms else "general_ai_news" 
                    query_part = "".join(c if c.isalnum() or c in "-_ " else "_" for c in query_part)  
                    filename = f"{search_date}_{query_part}.json"
                    
                    # Save to JSON file
                    file_path = os.path.join(save_dir, filename)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump({
                            "query": query,
                            "search_date": search_date,
                            "articles": normalized_articles
                        }, f, indent=2, ensure_ascii=False)
                    
                    print(f"Search results saved to: {filename}")
                
                return normalized_articles
            else:
                print(f"Error fetching news: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return []
class NewsSummarizerTools:
    """Tool for summarizing AI news articles."""
    
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.prompt_template = """
Analyze this AI news article and provide:
1. A concise 5-9 sentence summary highlighting key innovations and significance
2. An importance rating (1-10): Exemple a news that explane general information about the fild of AI is will be classify as a 4, since this is just general information that you can fine whit a webserch. Now, an article that talks about how a model is being applied in an area in an innovative way or about a new model will be considered a 9 or more depending on the content, because it is bringing a new perspective to the area.
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

    def summarize_article(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Summarizes a news article with importance rating and key points."""
        # Extract the basic fields
        title = article_data.get("title", "Untitled")
        description = article_data.get("description", "")
        content = article_data.get("content", "")
        
        # If there's no text, return early
        if not (title or description or content):
            return {
                **article_data,
                "summary": "No content available for summarization.",
                "importance_score": 0,
                "key_points": []
            }

        # Create the prompt with the article content
        final_prompt = self.prompt_template.format(
            title=title,
            description=description,
            content=content
        )

        try:
            # Generate the summary using OpenAI
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
                temperature=0.3
            )

            result = response.choices[0].message.content.strip()
            
            # Parse the response
            summary_text = "Summary not generated."
            importance_score = 5
            key_points = []
            
            for line in result.split("\n"):
                line = line.strip()
                if line.startswith("SUMMARY:"):
                    summary_text = line[len("SUMMARY:"):].strip()
                elif line.startswith("IMPORTANCE:"):
                    try:
                        importance_score = int(line[len("IMPORTANCE:"):].strip())
                    except ValueError:
                        importance_score = 5
                elif line.startswith("KEY_POINTS:"):
                    raw_points = line[len("KEY_POINTS:"):].strip()
                    key_points = [point.strip() for point in raw_points.split(",") if point.strip()]

            # Return the result with original data preserved
            return {
                **article_data,
                "summary": summary_text,
                "importance_score": importance_score,
                "key_points": key_points
            }
        except Exception as e:
            print(f"Error summarizing article: {str(e)}")
            return {
                **article_data,
                "summary": f"Summary unavailable due to an error: {str(e)}",
                "importance_score": 5,
                "key_points": []
            }

    def batch_summarize_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Summarize a batch of articles and return them with summaries."""
        return [self.summarize_article(article) for article in articles]

class NewsTrendAnalyzerTools:
    def analyze_trends(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract trends from the articles."""
        if not articles:
            return {}

        # Extract key points and title words
        key_point_counts = {}
        title_word_counts = {}
        
        # Words to exclude
        stop_words = {
            'and', 'the', 'to', 'of', 'in', 'for', 'with', 'on', 'at', 'from', 'by', 'about', 
            'as', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'how', 'what', 
            'when', 'where', 'who', 'why', 'which', 'that', 'this', 'these', 'those'
        }
        
        for article in articles:
            # Process title words
            if title := article.get("title"):
                title_lower = ''.join(c if c.isalnum() or c.isspace() else ' ' for c in title.lower())
                words = [w for w in title_lower.split() if len(w) > 3 and w not in stop_words]
                
                # Extract potential multi-word phrases (bigrams)
                if len(words) > 1:
                    for i in range(len(words) - 1):
                        bigram = f"{words[i]} {words[i+1]}"
                        title_word_counts[bigram] = title_word_counts.get(bigram, 0) + 1
                
                # Also count individual words
                for word in words:
                    title_word_counts[word] = title_word_counts.get(word, 0) + 1
            
            # Process key points
            for point in article.get("key_points", []):
                if isinstance(point, str):
                    point_lower = point.lower().strip()
                    
                    if len(point_lower) > 3 and not any(c in point_lower for c in [',', ';']):
                        key_point_counts[point_lower] = key_point_counts.get(point_lower, 0) + 2
                    
                    for term in point_lower.split(','):
                        term = term.strip()
                        if term and len(term) > 3 and term not in stop_words:
                            key_point_counts[term] = key_point_counts.get(term, 0) + 1

        # Combine key points and title words
        all_topics = {}
        all_topics.update(title_word_counts)
        
        for term, count in key_point_counts.items():
            all_topics[term] = all_topics.get(term, 0) + count * 2
        
        # Get top topics
        trending_topics = sorted(
            [(topic, count) for topic, count in all_topics.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Deduplicate - remove topics that are substrings of others
        filtered_topics = []
        for topic1, count1 in trending_topics:
            if not any(
                topic1 != topic2 and topic1 in topic2 and count1 <= count2 
                for topic2, count2 in filtered_topics
            ):
                filtered_topics.append((topic1, count1))
        
        # Take up to 5 trending topics
        final_topics = [topic for topic, _ in filtered_topics[:5]]
        
        # Get top articles
        top_articles = sorted(articles, key=lambda x: x.get("importance_score", 0), reverse=True)[:3]

        # Calculate average importance
        importance_scores = [a.get("importance_score", 0) for a in articles if "importance_score" in a]
        avg_importance = sum(importance_scores) / len(importance_scores) if importance_scores else 0

        return {
            "trending_topics": final_topics,
            "top_articles": [
                {"title": a.get("title", "Untitled"), "score": a.get("importance_score", 0)}
                for a in top_articles
            ],
            "average_importance": avg_importance
        }

class CombinedSummaryTools:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        
    def extract_trending_topics(self, articles: List[Dict[str, Any]]) -> List[str]:
        """Extract the most common topics from the articles to guide the summary."""
        topic_counts = {}
        
        for article in articles:
            for point in article.get("key_points", []):
                if isinstance(point, str):
                    point = point.lower().strip()
                    topic_counts[point] = topic_counts.get(point, 0) + 1
        
        top_topics = sorted(
            [(topic, count) for topic, count in topic_counts.items()], 
            key=lambda x: x[1], 
            reverse=True
        )[:8]
        
        return [topic for topic, _ in top_topics]
        
    def generate_combined_summary(self, articles: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive summary of all articles."""
        if not articles:
            return "No articles available to summarize."
        
        sorted_articles = sorted(articles, key=lambda x: x.get("importance_score", 0), reverse=True)
        
        article_data = []
        for idx, article in enumerate(sorted_articles[:15]):
            title = article.get("title", "Untitled")
            summary = article.get("summary", "No summary available")
            importance = article.get("importance_score", 0)
            key_points = article.get("key_points", [])
            
            article_info = f"Article {idx+1} [Importance: {importance}/10]\nTitle: {title}\nSummary: {summary}\n"
            if key_points:
                article_info += f"Key Points: {', '.join(key_points)}\n"
            
            article_data.append(article_info)
        
        articles_text = "\n".join(article_data)
        
        trending_topics = self.extract_trending_topics(sorted_articles)
        topics_text = ", ".join(trending_topics) if trending_topics else "No clear trending topics identified."
        
        prompt = f"""
You are an AI research analyst tasked with creating a comprehensive executive summary of recent AI developments for technology enthusiasts and professionals. 
Your goal is to synthesize information from multiple articles into a coherent, non-redundant summary that highlights the most significant advancements.

ARTICLES:
{articles_text}

TRENDING TOPICS: 
{topics_text}

INSTRUCTIONS:
1. Begin with a brief high-level overview of the current state of AI based on these articles.
2. Focus on the most important developments (articles with higher importance scores).
3. Group related technologies and themes rather than summarizing each article individually.
4. Highlight genuine breakthroughs, practical applications, and emerging trends.
5. Mention specific companies, researchers, or models only if they're making significant contributions.
6. Use precise technical language appropriate for AI enthusiasts without unnecessary jargon.
7. Identify patterns or contradictions across articles that reveal deeper insights about industry direction.
8. End with 1-2 sentences on what these developments collectively suggest about the near future of AI.

Format your response as a cohesive 3-4 paragraph summary. DO NOT use bullet points, numbered lists, or article references.
Ensure the summary is informative, forward-looking, and valuable for someone wanting to stay updated on AI advancements.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert AI research analyst who specializes in identifying significant trends and developments in artificial intelligence."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=800
            )
            
            combined_summary = response.choices[0].message.content.strip()
            return combined_summary
            
        except Exception as e:
            print(f"Error generating combined summary: {str(e)}")
            return "Unable to generate a combined summary at this time."

# Create CrewAI Agents using our tools
news_extractor_agent = Agent(
    role="AI News Extractor",
    goal="""Retrieve the latest AI news from reputable sources,considering the time period of this and the previous week.
    Focusing on articles about new research, tools and discoveries""",
    backstory="""Expert AI professor with years of experience tracking AI industry trends,
    with a passion for sharing new and relevant information in the field with their colleagues.""",
    verbose=True,
    allow_delegation=True
)

news_summarizer_agent = Agent(
    role="AI News Analyzer and Summarizer",
    goal="Create insightful summaries of AI news that highlight true significance, filter out hype and product advertising.",
    backstory="""Distinguished AI researcher with expertise in evaluating and contextualizing 
    new developments in AI. Exceptional at distilling complex technical information into 
    accessible insights while maintaining technical accuracy.""",
    verbose=True,
    allow_delegation=True
)

trend_analyzer_agent = Agent(
    role="AI Trend Analyst",
    goal="Identify emerging patterns and significant developments in AI technology.",
    backstory="""Experienced technology trend analyst with a specialization in artificial intelligence.
    Known for spotting important patterns before they become mainstream and separating meaningful
    signals from market noise.""",
    verbose=True,
    allow_delegation=True
)

executive_summarizer_agent = Agent(
    role="Executive AI Insights Specialist",
    goal="Create comprehensive overviews of AI developments for busy professionals.",
    backstory="""Former technology executive turned AI researcher who specializes in creating 
    high-value summaries that capture the most important developments in the field.
    Expert at contextualizing individual news items within broader industry trends.""",
    verbose=True,
    allow_delegation=True
)