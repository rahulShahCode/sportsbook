from constants import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_SECRET, ACCESS_KEY
import oauth2 
from urllib.parse import quote 

tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
def oauth_init(key,secret):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    return oauth2.Client(consumer,token)

def post_tweet(client,status):
    o = quote(status)
    resp,content = client.request(tweet_url + f"?status={o}", method="POST")
    return content 

client = oauth_init(ACCESS_KEY, ACCESS_SECRET)
