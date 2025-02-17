from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from typing import Dict, List
import json

# Initialize Ollama with the model
llm = OllamaLLM(
    model="llama3.1:8b",  # Use your specific model
    temperature=0.1,
    format="json"
)

# Create a more refined prompt template for sentiment analysis
SENTIMENT_TEMPLATE = """
You are a professional cryptocurrency market analyst with expertise in sentiment analysis and market trends. Your task is to analyze Reddit discussions about {coin_name} and provide an objective analysis.

Context:
- Coin Name: {coin_name}
- Number of Posts Analyzed: {post_count}
- Time Frame: Recent discussions

Reddit Discussions to Analyze:
{reddit_posts}

Instructions:
1. Carefully read each post and its engagement metrics
2. Consider the following aspects:
   - Overall community sentiment
   - Technical discussion quality
   - Concerns and criticisms
   - Development and adoption potential
   - Market speculation patterns
3. Identify recurring themes and significant points
4. Evaluate the credibility of discussions
5. Assess risk factors and growth opportunities

Provide your analysis in the following JSON format, ensuring each field is properly filled:
{
    "overall_sentiment": "<CHOOSE ONE: positive/neutral/negative>",
    "confidence_score": "<NUMBER 0-100>",
    "key_points": [
        "Most significant discussion points",
        "Notable community concerns",
        "Prominent technical aspects"
    ],
    "risks": [
        "Identified risk factors",
        "Potential vulnerabilities"
    ],
    "opportunities": [
        "Growth potential",
        "Development milestones",
        "Market advantages"
    ],
    "recommendation": "<CONCISE actionable trading or investment recommendation>"
}

Requirements:
- Be objective and data-driven in your analysis
- Base conclusions on the provided discussions only
- Maintain professional analytical language
- Ensure the response is in valid JSON format
- Provide specific, not generic, insights
- Consider both technical and sentiment factors

Analysis:
"""

sentiment_prompt = PromptTemplate(
    input_variables=["coin_name", "reddit_posts", "post_count"],
    template=SENTIMENT_TEMPLATE
)

def format_reddit_posts(posts: List[Dict]) -> str:
    """Format Reddit posts into a structured, easy-to-analyze format."""
    formatted_posts = []
    for i, post in enumerate(posts, 1):
        formatted_post = f"""
[Post {i}]
TITLE: {post['title']}
CONTENT: {post['description'][:500] if post['description'] else 'No content'}
ENGAGEMENT: {post['votes']} votes
SENTIMENT INDICATORS: {'Positive' if post['votes'] > 10 else 'Neutral' if post['votes'] >= 0 else 'Negative'}
---"""
        formatted_posts.append(formatted_post)
    return "\n".join(formatted_posts)

def analyze_coin_sentiment(coin_name: str, reddit_posts: List[Dict]) -> Dict:
    """Analyze sentiment for a single coin using the LLM."""
    try:
        # Format the Reddit posts
        formatted_posts = format_reddit_posts(reddit_posts)
        post_count = len(reddit_posts)
        
        # Generate the prompt with post count
        prompt = sentiment_prompt.format(
            coin_name=coin_name,
            reddit_posts=formatted_posts,
            post_count=post_count
        )
        
        # Get LLM response
        response = llm.invoke(prompt)
        
        # Parse JSON response
        try:
            analysis = json.loads(response)
            # Validate required fields
            required_fields = ['overall_sentiment', 'confidence_score', 'key_points', 
                             'risks', 'opportunities', 'recommendation']
            if not all(field in analysis for field in required_fields):
                raise json.JSONDecodeError("Missing required fields", response, 0)
            
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON response for {coin_name}. Using fallback analysis.")
            analysis = {
                "overall_sentiment": "neutral",
                "confidence_score": "0",
                "key_points": [
                    "Error parsing LLM response",
                    "Analysis needs manual review",
                    "Data quality insufficient"
                ],
                "risks": ["Unable to determine risks due to parsing error"],
                "opportunities": ["Manual analysis recommended"],
                "recommendation": "Insufficient data for automated analysis. Please review manually."
            }
        
        return analysis
        
    except Exception as e:
        print(f"Error analyzing {coin_name}: {str(e)}")
        return None

def generate_full_report(coin_discussions: Dict[str, List[Dict]]) -> Dict[str, Dict]:
    """Generate comprehensive sentiment analysis report for all coins."""
    report = {}
    
    for coin_name, posts in coin_discussions.items():
        print(f"\nAnalyzing sentiment for {coin_name}...")
        analysis = analyze_coin_sentiment(coin_name, posts)
        if analysis:
            report[coin_name] = analysis
            print(f"Completed analysis for {coin_name}")
    
    return report

if __name__ == "__main__":
    from coin_analyzer import analyze_new_coins
    
    print("Starting cryptocurrency sentiment analysis...")
    coin_discussions = analyze_new_coins()
    
    if not coin_discussions:
        print("No coin discussions found to analyze.")
        exit()
    
    print("\nGenerating sentiment analysis report...")
    report = generate_full_report(coin_discussions)
    
    print("\nFinal Analysis Report:")
    for coin, analysis in report.items():
        print(f"\n{'='*50}")
        print(f"Analysis for {coin}")
        print(f"{'='*50}")
        print(f"Overall Sentiment: {analysis['overall_sentiment']}")
        print(f"Confidence Score: {analysis['confidence_score']}")
        print("\nKey Points:")
        for point in analysis['key_points']:
            print(f"• {point}")
        print("\nRisks:")
        for risk in analysis['risks']:
            print(f"• {risk}")
        print("\nOpportunities:")
        for opp in analysis['opportunities']:
            print(f"• {opp}")
        print(f"\nRecommendation: {analysis['recommendation']}")
        print(f"{'='*50}")
