from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import sys
import datetime

OUTPUT_FILE="new_tweets.txt"
CONSUMER_SECRET="oKsGTjajzKBiFGjxVJGb7mh0RlTtLwS8TlfORTnBZlsVcKyuwz"
CONSUMER_KEY="gc5jBYM3eC3wFFI4pLipSvvU9"
TOKEN_SECRET="nHmgTX56HKaIFAKD3QQjHtbuaax0xGXOkeB32hS1XBBvy"
TOKEY_KEY="2841234509-OvgVEOHCcSgo5cNuRBzU1wnQFR4gpzKg4PaXU6w"

f = open(OUTPUT_FILE, "a")
tmpData = ""
tweet_count = 0
class StdOutListener(StreamListener):
    def on_data(self, data):
        global tweet_count
        global f
        global tmpData
        try: 
            if data == "":
               return
            tmp = json.loads(data)
            if tmp == None:
                return
            if "created_at" not in tmp:
                return
            coords = [0,0]
            created_at = tmp["created_at"]
            if "coordinates"  in tmp:
                if tmp["coordinates"] != None:
                    if "coordinates" in tmp["coordinates"]:
                        coords = tmp["coordinates"]["coordinates"]
            ids =  tmp["id"]
            text = tmp["text"]
            ## Get rid of UTF non-sense....
            text = text.encode('ascii', 'ignore').decode('ascii')
            text.replace("|","[replaced bar]")
            text.replace("\n", " ")
            #p = str(idource venv/bin/activate) + "|" + str(created_at) + "|" + str(coords[0]) + "|" + str(coords[1]) + "|" + str(text) + "\n"
            p = str(text) + "<END OF TWEET/>\n"
            #print p
            #if len(p) > 80:
            #    print p[:79]
            #else:
            #    print p
            tmpData = tmpData + p
            #f.write(p)
            tweet_count += 1
            if tweet_count % 1000 == 0:
                f.write(tmpData)
                print "writing and flushing data"
                f.flush()
                tmpData = ""
                print  str(datetime.datetime.now()) + " --- TWITTER_COUNT = " + str(tweet_count)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print "ERROR - " + str(e)
            print exc_tb.tb_lineno

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(TOKEY_KEY, TOKEN_SECRET)
    stream = Stream(auth, l)
    stream.filter(track=['#programming','#google','#android'])
    stream.sample()
    #locations=[-129.19,23.96,-64.68,50.68]
