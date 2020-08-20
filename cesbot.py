import tweepy
import time

auth = tweepy.OAuthHandler('','')
auth.set_access_token('','' )

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


user = api.me()

search = '100DaysOfCode', 'CodeNewbie'
nrTweets = 100

for tweet in tweepy.Cursor(api.search, search).items(nrTweets):
    try:
        print('Tweet retweeted')
        tweet.retweet()
        tweet.favorite()
        time.sleep(10)
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break
