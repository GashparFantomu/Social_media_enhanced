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


def publica_pe_facebook(text_postare, page_access_token, page_id):
    """Publică un mesaj pe o Pagină de Facebook."""
    url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {
        "message": text_postare,
        "access_token": page_access_token
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            mesaj = "SUCCES FACEBOOK: Postare publicată!"
            print(f"✅ {mesaj}")
            logging.info(mesaj)
            return True
        else:
            mesaj = f"EȘEC FACEBOOK: Cod {response.status_code}. {response.text}"
            print(f"❌ {mesaj}")
            logging.error(mesaj)
            return False
    except Exception as e:
        mesaj = f"EȘEC FACEBOOK (Rețea): {e}"
        print(f"❌ {mesaj}")
        logging.error(mesaj)
        return False


def publica_pe_threads(text_postare, threads_token):
    """Publică un mesaj pe Threads folosind Threads API (Meta)."""
    # Pasul 1: Creăm containerul pentru text
    url_container = "https://graph.threads.net/v1.0/me/threads"
    payload_container = {
        "media_type": "TEXT",
        "text": text_postare,
        "access_token": threads_token
    }

    try:
        # Trimitem textul către Meta
        response_c = requests.post(url_container, data=payload_container)
        if response_c.status_code != 200:
            mesaj = f"EȘEC THREADS (Container): {response_c.status_code} - {response_c.text}"
            print(f"❌ {mesaj}")
            logging.error(mesaj)
            return False

        # Dacă e succes, Meta ne dă un ID de container
        container_id = response_c.json().get("id")

        # Pasul 2: Publicăm containerul creat
        url_publish = "https://graph.threads.net/v1.0/me/threads_publish"
        payload_publish = {
            "creation_id": container_id,
            "access_token": threads_token
        }

        response_p = requests.post(url_publish, data=payload_publish)
        if response_p.status_code == 200:
            mesaj = "SUCCES THREADS: Postare publicată live!"
            print(f"✅ {mesaj}")
            logging.info(mesaj)
            return True
        else:
            mesaj = f"EȘEC THREADS (Publicare): {response_p.status_code} - {response_p.text}"
            print(f"❌ {mesaj}")
            logging.error(mesaj)
            return False

    except Exception as e:
        mesaj = f"EȘEC THREADS (Rețea): {e}"
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