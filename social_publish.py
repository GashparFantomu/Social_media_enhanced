import logging
import requests
import tweepy

logging.basicConfig(
    filename='social_publishing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def publica_pe_x(text_tweet):
    """Publică un mesaj pe X (Twitter)."""
    try:
        client = tweepy.Client(
            bearer_token="X_BEARER_TOKEN",
            consumer_key="X_API_KEY",
            consumer_secret="X_API_SECRET",
            access_token="X_ACCESS_TOKEN",
            access_token_secret="X_ACCESS_SECRET"
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


def publica_pe_linkedin(text_postare):
    """Publică un mesaj pe LinkedIn."""
    # Aceste date trebuie obținute din aplicația ta LinkedIn Developer
    LINKEDIN_TOKEN = "LINKEDIN_ACCESS_TOKEN"
    URN = "urn:li:person:ID_UL_TAU"

    url = "[https://api.linkedin.com/v2/ugcPosts](https://api.linkedin.com/v2/ugcPosts)"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    payload = {
        "author": URN,
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