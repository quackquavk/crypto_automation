from get_announcement import get_binance_announcements
from api import fetch_reddit_data
import time

def analyze_new_coins():
    new_coins = get_binance_announcements()
    if not new_coins:
        print("No new coins found")
        return
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
        
        time.sleep(2)
    
    for coin, posts in coin_discussions.items():
        print(f"\n{'='*40}")
        print(f"Discussions for {coin}:")
        print(f"{'='*40}")
        
        for i, post in enumerate(posts, 1):
            print(f"\nPost {i}:")
            print(f"Title: {post['title']}")
            print(f"Description: {post['description'][:200]}..." if len(post['description']) > 200 
                  else f"Description: {post['description']}" if post['description'] 
                  else "Description: [No description]")
            print(f"Votes: {post['votes']}")
    
    return coin_discussions

if __name__ == "__main__":
    analyze_new_coins()