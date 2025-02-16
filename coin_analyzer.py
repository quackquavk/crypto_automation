from get_announcement import get_binance_announcements
from api import fetch_reddit_data
import time

def analyze_new_coins():
    # Step 1: Get new coin listings from Binance
    new_coins = get_binance_announcements()  # This returns ["coin1", "coin2", ...]
    if not new_coins:
        print("No new coins found")
        return
    
    # Store results for all coins
    coin_discussions = {}
    
    # Step 2: For each coin, fetch Reddit discussions
    for coin in new_coins:
        print(f"\nAnalyzing discussions for {coin}...")
        search_query = f"{coin}"
        posts = fetch_reddit_data(query=search_query)
        
        if posts:
            coin_discussions[coin] = posts
            print(f"Found {len(posts)} discussions for {coin}")
        else:
            print(f"No discussions found for {coin}")
        
        # Respect Reddit's rate limits
        time.sleep(2)
    
    # Print and return results
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