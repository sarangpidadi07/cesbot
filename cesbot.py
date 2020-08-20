import tweepy
import time

auth = tweepy.OAuthHandler('AHaWmU2sWY8ovXolzHgZq5JGw','C5LhjudsLeQkpVUzry12MjpbcdzbT2Z2KqFm8GbgoQqDvReMkm')
auth.set_access_token('1295218750627536900-mTs3PnwFUrNvVJMRwP7yPyON0Ewp1K','soLJOxhLeqz49zSeW1HeuDyJIsYW6O64j4QqqYUgF4Pii' )

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


user = api.me()

search = 'javascript' or 'python' or '100DaysOfCode' or '@sarangpidadi07' or 'CodeNewbie'
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
