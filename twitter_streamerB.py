from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import sys
import datetime

OUTPUT_FILE="new_tweets_timeB.txt"
CONSUMER_SECRET="ZK2MlkA7xmqCqzVxo21gXrWdl56Na6GtgFNBWdUUPWsPwAWUJU"
CONSUMER_KEY="TZtTf8KBUokZwqpS0y9gzm7zM"
TOKEN_SECRET="wqbfALgDuYZixO6IwfaJZwMcIOCStg7Cl8Dg5uOyvGWd2"
TOKEY_KEY="2841234509-8MKVhmeay4H22n5k5IQGyuqpjijlSsZzVJiqB1f"

f = open(OUTPUT_FILE, "a")
tmpData = ""
tweet_count = 0
class StdOutListener(StreamListener):
    #streamG =1
    #def setStream(self,streamx):
    #    global streamG
    #    streamG = streamx
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
	    user = tmp["user"]
	    screen_name = user["screen_name"]
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
            p = "<"+str(screen_name)+"> | "+str(created_at)+" | "+str(text) + " <END OF TWEET>\n"
            #print str(tweet_count)+":::"+p
            #if len(p) > 80:
            #    print p[:79]
            #else:
            #    print p
            tmpData = tmpData + p
            #f.write(p)
            tweet_count += 1
            if tweet_count % 100 == 0:
                print str(tweet_count)
                #streamG.dissconnect()
                f.write(tmpData)
                print "writing and flushing data"
                f.flush()
                f.close()
                f = open(OUTPUT_FILE, "a")
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
    print "Successfully authenticated - N.B. if 420 print then we are being rate limited"
    stream = Stream(auth, l)
    #l.setStream(stream)
    stream.filter(track=['#programming','#google','#android','#apple'])
    stream.sample()
    stream.disconnect()
    #locations=[-129.19,23.96,-64.68,50.68]
