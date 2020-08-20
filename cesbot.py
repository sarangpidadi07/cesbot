import os
import redis
import time
import schedule

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
key = os.getenv("KEY")
secret = os.getenv("SECRET")

client = redis.Redis(host="Your IP adress", port=6379,
                     password=os.getenv("REDIS_PASS"))
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
auth.secure = True
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def read_last_seen():
    last_seen_id = int(client.get('last_seen_id'))
    return last_seen_id


def store_last_seen(last_seen_id):
    client.set('last_seen_id', str(last_seen_id))
    return


def reply():
    tweets = api.mentions_timeline(
        read_last_seen(), tweet_mode='extended')
    for tweet in reversed(tweets):
        try:
            username = tweet.user.screen_name

            print("Replied to - " + username +
                  " - " + tweet.full_text)
            api.update_status("@" + username +
                              " Hello, " + username + ", this is an auto reply :)", tweet.id)

            print("Favorited " + username + " - " + tweet.full_text)
            api.create_favorite(tweet.id)
            store_last_seen(tweet.id)
        except tweepy.TweepError as e:
            store_last_seen(tweet.id)
            print(e.reason)
            time.sleep(2)

search = '100DaysOfCode', 'CodeNewbie'
nrTweets = 100
def searchTwit():
    for tweet in tweepy.Cursor(api.search, search).items(nrTweets):
        try:
            print('Tweet retweeted')
            tweet.retweet()
            tweet.favorite()
            time.sleep(5)
        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(5)
        except StopIteration:
            break

# Schedule the functions to run 
schedule.every(15).minutes.do(reply)
schedule.every().day.at("12:00").do(searchTwit)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except tweepy.TweepError as e:
        print(e.reason)
        time.sleep(1)
