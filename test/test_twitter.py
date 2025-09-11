import os, tweepy
from dotenv import load_dotenv

load_dotenv()
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
)
# Test credentials first
try:
    resp = client.get_me(user_auth=True)
    print("✅ Authenticated as:", resp.data.username)
except Exception as e:
    print("❌ Auth error:", e)

# Then post the tweet
try:
    response = client.create_tweet(
        text="Hello from X API v2 with user_auth PNG 🐦",
        user_auth=True
    )
    print("✅ Tweet posted:", response.data)
except Exception as e:
    print("❌ Tweet error:", e)
