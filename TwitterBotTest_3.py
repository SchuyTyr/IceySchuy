import tweepy
from time import sleep
from tweepybots.credentials import *
import logging
from datetime import datetime

print("Program running...")

## Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

## Create API object
api = tweepy.API(auth)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

## Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
            # if not tweet.favorited:
            ## Mark it as Liked, since we have not done it yet
            # try:
                # tweet.favorite()
            # except Exception as e:
            #    logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

now = datetime.now().time()
#'183058979', 
ids = ['3076649353', '3006430517', '3006481618', '3006403895', '3003374135', '68227206', '1252862957182046208'] #4173434831,743638086534455296,3374878756
while True:
    sleep(5)
    print("Starting at =", now)
    for i in ids:
        #for tweet in tweepy.Cursor(api.user_timeline,id='183058979').items(1):
        #(i,count = 2,trim_user = False, exclude_replies = True, include_rts = True)
        # 6 items for Season 6
        for tweet in tweepy.Cursor(api.user_timeline,i).items(15):
            try:
                if tweet.in_reply_to_status_id is not None:
                    # This tweet is a reply or I'm its author so, ignore it
                    print("Is Reply...")
                    # Add \n escape character to print() to organize tweets
                    #print('\nTweet by: @' + tweet.user.screen_name)
                else:
                    try:
                        tweet.retweet()
                        print("Retweeted")
                    except Exception as e:
                        print("Already Retweeted")
                print("i = " + i + ', Tweet by: @' + tweet.user.screen_name)
                #sleep(5)

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break
    now = datetime.now().time()
    print("Sleeping at =", now)
    print("Currently sleeping....zzzzz")        
    sleep(6000)

#print("Test Complete.")