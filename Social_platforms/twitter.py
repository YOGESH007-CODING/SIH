import os
import tweepy
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Twitter Auth Setup
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
)

# v1.1 Auth (needed for media upload)
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_SECRET")
)
api_v1 = tweepy.API(auth)
class Social_Handles():
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
    def build_tweet_text(self, state):
        Metadata=state['metadata']
        address = Metadata['Address']
        # road = address.get("road", "Unknown road")
        # city = address.get("city", "Unknown city")
        # country = address.get("country", "Unknown country")
        # date = Metadata.get("datetime", "Unknown date").split(" ")[0]
        # issue_id = state.get("issue_id", "unknown_id")
        similar_issue = state["similar_count"]

        prompt = f"""
                You are generating a tweet to report a civic issue to the city municipality.

                The **exact location details (e.g., road or ward)** are incomplete or missing in the available data. However, the full details—including image, coordinates, and description—have already been sent via email to the appropriate civic authority.

                Based on the following information:
                - Issue type : {state.get("issue_type", "Unknown_issue")}
                - Report Date: {state.get("metadata", {}).get("datetime", "Unknown date").split(" ")[0]}
                - Issue ID: {state.get("issue_id", "unknown_id")}
                - Address: {state.get("metadata", {}).get("Address", {})}
                - Similar issue reported nearby: {state.get("similar_count", 0)}
                - Submitted via photo
                - Email sent to: {state.get("Authority_info", {}).get("Email", "authority@example.com")}

                **Generate a professional and citizen-friendly tweet** that:
                1. Brings the issue to the municipality’s attention.
                2. Mentions that full details have already been shared via email.
                3. Refers to the municipal body using a general reference (e.g., “city authorities” or “local officials”), not @mentions.
                4. Includes relevant hashtags like #CivicIssue, #UrbanIndia, #SmartCity.
                5. Uses relevant and catchy emojis.
                6. Adds a light, respectful touch of humor to encourage faster resolution.
                7. Keeps the message under 280 characters.
                8. Avoids tagging specific people or using @ handles.
                9. Refers to the authority by name only—not full email addresses.

                Return only the tweet text. No explanation or formatting outside the tweet.
                """

        response = self.model.generate_content(prompt)
        return response.text
    def make_tweet_info(self, state):
        tweet_text = self.build_tweet_text(state)

        return tweet_text
    def post_issue_to_twitter(self, state):
        if state['approvals']['tweet_review'] == False:
            return {'status': 'pending', 'text': None, 'url': None}

        tweet_text=state['tweet']['text']
        tweet_status={'status': 'pending', 'text': tweet_text, 'url': None}
        image_paths = state.get("image_paths")

        # for image_path in image_paths:
        #     if not os.path.exists(image_path):
        #         print("❌ Image path is invalid or file does not exist:", image_paths)
        #         return

        try:
            # Upload image via v1.1 API
            # media = api_v1.media_upload(image_path)
            # response = client.create_tweet(
            #     text=tweet_text,
            #     media_ids=[media.media_id_string],
            #     user_auth=True
            # )
            max_images = 3
            media_ids = []

            for image_path in image_paths[:min(len(image_paths), max_images)]:
                media = api_v1.media_upload(image_path)
                media_ids.append(media.media_id_string)

            # Build and post the tweet
            response = client.create_tweet(
                text=tweet_text,
                media_ids=media_ids,
                user_auth=True
            )

            tweet_url=f"https://twitter.com/user/status/{str(response.data['id'])}"
            print("✅ Tweet posted successfully!")
            # print("🔗 Tweet URL:"+ tweet_url)
            tweet_status['status']="completed"
            tweet_status['url'] = tweet_url
            return tweet_status

        except Exception as e:
            tweet_status['status'] = "Failed"
            print("❌ Failed to post tweet:", e)
            return tweet_status

if __name__ == "__main__":
    from pprint import pprint

    # Create dummy state
    test_state = {
        "image_path": "E:/CivicSpotter/test/photo_extractor/test_data/test_photo.jpg",  # ✅ Update with actual path
        "issue_id": "faridabad_20250619_001",
        "metadata": {
            "datetime": "2025:06:19 12:30:00",
            "Address": {
                "road": "Hisar Road",
                "city": "Faridabad",
                "country": "India"
            }
        }
    }

    handler = Social_Handles()
    handler.post_issue_to_twitter(test_state)
