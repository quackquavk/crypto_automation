import requests
import json
import time

def fetch_reddit_data(query="bitcoin", access_token=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    url = f"https://www.reddit.com/search.json?q={query}&limit=10"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        posts = []
        for post in data["data"]["children"]:
            post_data = post["data"]
            posts.append(
                {
                    "title": post_data["title"],
                    "description": post_data.get("selftext", ""),
                    "votes": post_data.get("score", 0),
                }
            )

        return posts

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
