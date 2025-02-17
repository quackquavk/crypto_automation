from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from typing import Dict, List
import json

# Initialize Ollama with the model
llm = OllamaLLM(
    model="llama3.1:8b",  # Change this to "llama2:13b" or your specific model "llama3.1:8b"
    temperature=0.1,  # Lower temperature for more consistent outputs
    format="json"  # Request JSON format specifically
)

# Modify the template to be more explicit about JSON formatting
SENTIMENT_TEMPLATE = """
You are a professional cryptocurrency market analyst. Analyze the Reddit discussions about {coin_name} and provide an analysis in VALID JSON format.

Context:
- Coin Name: {coin_name}
- Number of Posts: {post_count}
- Time Frame: Recent discussions

Reddit Discussions:
{reddit_posts}

RESPOND ONLY WITH A VALID JSON OBJECT in this exact format:
{{
    "overall_sentiment": "positive/neutral/negative",
    "confidence_score": "0-100",
    "key_points": [
        "point1",
        "point2",
        "point3"
    ],
    "risks": [
        "risk1",
        "risk2"
    ],
    "opportunities": [
        "opportunity1",
        "opportunity2"
    ],
    "recommendation": "brief recommendation"
}}

Ensure your response is ONLY the JSON object, with no additional text or formatting.
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
        
        # Generate the prompt
        prompt = sentiment_prompt.format(
            coin_name=coin_name,
            reddit_posts=formatted_posts,
            post_count=post_count
        )
        
        # Get LLM response
        response = llm.invoke(prompt)
        
        # Clean the response if needed (remove any leading/trailing whitespace and newlines)
        if isinstance(response, str):
            response = response.strip()
            
            # Try to find JSON content
            try:
                # Find the first '{' and last '}'
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    response = response[start:end]
            except:
                pass
        
        # Parse JSON response
        try:
            if isinstance(response, dict):
                analysis = response
            else:
                analysis = json.loads(response)
                
            # Validate required fields
            required_fields = ['overall_sentiment', 'confidence_score', 'key_points', 
                             'risks', 'opportunities', 'recommendation']
            if not all(field in analysis for field in required_fields):
                raise json.JSONDecodeError("Missing required fields", str(response), 0)
            
            return analysis
            
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Warning: Invalid JSON response for {coin_name}. Error: {str(e)}")
            return {
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
