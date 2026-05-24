import logging
import requests
import tweepy

logging.basicConfig(
    filename='social_publishing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def publica_pe_x(text_tweet, api_key, api_secret, access_token, access_secret):
    """Publică un mesaj pe X (Twitter) folosind credențialele utilizatorului."""
    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        response = client.create_tweet(text=text_tweet)
        mesaj = f"SUCCES X: Tweet publicat (ID: {response.data['id']})"
        print(f"✅ {mesaj}")
        logging.info(mesaj)
        return True
    except Exception as e:
        mesaj = f"EȘEC X: {e}"
        print(f"❌ {mesaj}")
        logging.error(mesaj)
        return False


def publica_pe_linkedin(text_postare, user_token, user_urn):
    """Publică un mesaj pe LinkedIn folosind credențialele utilizatorului."""
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {user_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    payload = {
        "author": user_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text_postare},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            mesaj = "SUCCES LINKEDIN: Postare publicată!"
            print(f"✅ {mesaj}")
            logging.info(mesaj)
            return True
        else:
            mesaj = f"EȘEC LINKEDIN: Cod {response.status_code}. {response.text}"
            print(f"❌ {mesaj}")
            logging.error(mesaj)
            return False
    except Exception as e:
        mesaj = f"EȘEC LINKEDIN (Rețea): {e}"
        print(f"❌ {mesaj}")
        logging.error(mesaj)
        return False