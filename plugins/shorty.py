import os
import requests
import logging
import pyshorteners
import tiny
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

urlshortx_api_token = os.getenv("URL_SHORTENER_API_KEY")
s = pyshorteners.Shortener()


def shorten_url(url):
    """Shortens a URL using URLShortx first, then TinyURL."""
    try:
        # Shorten URL with URLShortx
        api_url = f"https://urlshortx.com/api"
        params = {"api": urlshortx_api_token, "url": url, "format": "text"}
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            urlshortx_url = response.text.strip()
        else:
            raise Exception("URL shortening with URLShortx failed.")

        # Shorten URLShortx URL with TinyURL
        short_url = s.tinyurl.short(urlshortx_url)
        logger.info(f'Shortened {url} to {short_url} using URLShortx and TinyURL.')
        return short_url
    except Exception as e:
        logger.error(f"URL shortening failed: {e}")
        return url
        
