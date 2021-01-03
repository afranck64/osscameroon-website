import requests
from requests.auth import HTTPBasicAuth
from app.settings import API_KEY, API_SECRET_KEY
import json
from app.main.utils.helpers.cache import Cache

# c = Cache()

def top_tweets(cache):
    """
    This method will return top-tweets
    comming from the request or just the cache

    params : the cache for the context
    return boolean telling if everything went well [top-tweets] as string
    """

    if cache.get("top-tweets") is None:
        try:
            # we make another request
            # to the twitter api
            tweets = requests.get(
              "https://api.twitter.com/1.1/search/tweets.json?q=#CaParleDev&result_type=popular",
              auth=HTTPBasicAuth(API_KEY, API_SECRET_KEY)
            ).content.decode()
            # and we cache it as json string
            cache.set("top-tweets", tweets, 10)
        except Exception as es:
            raise es
            return False, ""

    return True, cache.get("top-tweets")


def get_top_tweets(cache):
    """
    This method will check the return of top-tweet and send
    the appropriate status code for the request

    """

    results = top_tweets(cache)

    if results[0]:
        payload = json.loads(results[1])
        if "errors" in payload:
            return {
                "code": 500,
                "status": "error",
                "result": payload
            }
        else:
            return {
                "code": 200,
                "status": "success",
                "result": payload
            }
    else:
        return {
                "code": 500,
                "status": "error"
        }

