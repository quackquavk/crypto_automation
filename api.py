import os
from dotenv import load_dotenv
import requests
import json
import time

# Load environment variables
load_dotenv()


def get_reddit_access_token():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError(
            "REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET must be set in .env file"
        )

    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {
        "grant_type": "client_credentials",
    }
    headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}

    try:
        response = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data=data,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        print(f"Error getting access token: {e}")
        return None


def get_post_details(post_id, access_token):
    headers = {
        "User-Agent": "ChangeMeClient/0.1 by YourUsername",
        "Authorization": f"Bearer {access_token}",
    }
    url = f"https://oauth.reddit.com/api/info?id=t3_{post_id}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data["data"]["children"]:
            return data["data"]["children"][0]["data"].get("selftext", "")
        return ""

    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching post details: {e}")
        return ""


def fetch_reddit_data(query="bitcoin", access_token=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    url = f"https://www.reddit.com/search.json?q={query}+crypto&sort=relevance&t=month&limit=10"

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
