from get_announcement import get_binance_announcements
from api import fetch_reddit_data
from prompts import generate_full_report
import time
import json
from typing import Dict, List
import os

def analyze_new_coins(save_to_file: bool = True) -> Dict[str, Dict]:
    """
    Analyze new coins from Binance, fetch Reddit discussions, and generate sentiment analysis.
    Returns a complete analysis including Reddit posts and sentiment analysis.
    """
    # Step 1: Get new coin listings from Binance
    print("\n1. Fetching new coin listings from Binance...")
    new_coins =  ['solayer' , '1000chems' , 'Berachain'] # get_binance_announcements()
    if not new_coins:
        print("No new coins found")
        return {}

    # Step 2: Get Reddit discussions for each coin
    print("\n2. Fetching Reddit discussions...")
    coin_discussions = {}

    for coin in new_coins:
        print(f"\nAnalyzing discussions for {coin}...")
        search_query = f"{coin}"
        posts = fetch_reddit_data(query=search_query)
        
        if posts:
            coin_discussions[coin] = posts
            print(f"Found {len(posts)} discussions for {coin}")
        else:
            print(f"No discussions found for {coin}")
        
        time.sleep(2)  # Respect Reddit's rate limits

    if not coin_discussions:
        print("No Reddit discussions found for any coins")
        return {}

    # Step 3: Generate sentiment analysis
    print("\n3. Generating sentiment analysis...")
    analysis_report = generate_full_report(coin_discussions)

    # Combine Reddit posts with sentiment analysis
    complete_analysis = {}
    for coin in coin_discussions:
        if coin in analysis_report:
            complete_analysis[coin] = {
                "reddit_posts": coin_discussions[coin],
                "sentiment_analysis": analysis_report[coin]
            }

    # Save results to file if requested
    if save_to_file:
        save_analysis_report(complete_analysis)

    return complete_analysis

def save_analysis_report(analysis: Dict[str, Dict]):
    """Save the analysis report to a JSON file with timestamp."""
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"reports/coin_analysis_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=4, ensure_ascii=False)
        print(f"\nAnalysis saved to {filename}")
    except Exception as e:
        print(f"Error saving report: {str(e)}")

def print_analysis_report(analysis: Dict[str, Dict]):
    """Print a formatted version of the analysis report."""
    for coin, data in analysis.items():
        print(f"\n{'='*80}")
        print(f"ANALYSIS REPORT FOR {coin}")
        print(f"{'='*80}")
        
        sentiment = data['sentiment_analysis']
        print(f"\nSENTIMENT ANALYSIS:")
        print(f"Overall Sentiment: {sentiment['overall_sentiment']}")
        print(f"Confidence Score: {sentiment['confidence_score']}")
        
        print("\nKEY POINTS:")
        for point in sentiment['key_points']:
            print(f"• {point}")
        
        print("\nRISKS:")
        for risk in sentiment['risks']:
            print(f"• {risk}")
        
        print("\nOPPORTUNITIES:")
        for opp in sentiment['opportunities']:
            print(f"• {opp}")
        
        print(f"\nRECOMMENDATION: {sentiment['recommendation']}")
        
        print("\nREDDIT DISCUSSIONS:")
        for i, post in enumerate(data['reddit_posts'], 1):
            print(f"\nPost {i}:")
            print(f"Title: {post['title']}")
            print(f"Votes: {post['votes']}")
            if post['description']:
                desc = post['description'][:200] + "..." if len(post['description']) > 200 else post['description']
                print(f"Content: {desc}")
        
        print(f"\n{'='*80}")

if __name__ == "__main__":
    try:
        print("Starting comprehensive coin analysis...")
        analysis = analyze_new_coins()
        
        if analysis:
            print_analysis_report(analysis)
        else:
            print("No analysis generated.")
            
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")