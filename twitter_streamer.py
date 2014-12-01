import os
from multiprocessing import Pool, current_process
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import sys
import datetime


class StdOutListener(StreamListener):
    #streamG =1
    #def setStream(self,streamx):
    #    global streamG
    #    streamG = streamx
    def __init__(self, output_file):
        StreamListener.__init__(self)
        self.output_file = os.path.join("/scratch/data/", output_file)
        self.tmpData = ""
        self.tweet_count = 0

    def __exit__(self):
        self.f.close()

    def on_data(self, data):
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
            text.replace("\r", " ")
            #p = str(idource venv/bin/activate) + "|" + str(created_at) + "|" + str(coords[0]) + "|" + str(coords[1]) + "|" + str(text) + "\n"
            p = "<"+str(screen_name)+"> | "+str(created_at)+" | "+str(text) + " <END OF TWEET>\n"
            #print str(self.tweet_count)+":::"+p
            #if len(p) > 80:
            #    print p[:79]
            #else:
            #    print p
            self.tmpData = self.tmpData + p
            #f.write(p)
            self.tweet_count += 1
            if self.tweet_count % 1000 == 0:
                print str(self.tweet_count)
                #streamG.dissconnect()
                output_file = "%s.%s.txt" % (self.output_file, datetime.date.today().isoformat())
                with open(output_file, 'a') as f:
                    f.write(self.tmpData)
                print "writing and flushing data"
                self.tmpData = ""
                print str(datetime.datetime.now()) + " --- TWITTER_COUNT = " + str(self.tweet_count)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print "ERROR - " + str(e)
            print exc_tb.tb_lineno

    def on_error(self, status):
        print status


def run(args):
    pid = current_process().pid
    round = 1
    while True:
        try:
            l = StdOutListener(args['output_file'])
            auth = OAuthHandler(args['consumer_key'], args['consumer_secret'])
            auth.set_access_token(args['token_key'], args['token_secret'])
            print "%i's %i authentication success. (420 means rate limited)" % (pid, round)
            stream = Stream(auth, l)
            #l.setStream(stream)
            #stream.filter(track=['#programming','#google','#android'])
            stream.sample()
            #locations=[-129.19,23.96,-64.68,50.68]
        except KeyboardInterrupt:
            print "KeyboardInterrupt sensed, %i exiting..." % pid
            stream.disconnect()
            return True
        except Exception as e:
            print e
        finally:
            stream.disconnect()
            round += 1


if __name__ == '__main__':
    accounts = [{
        'output_file': "new_tweets_time.txt",
        'consumer_secret': "VnYHz2idN9Ymp52UVp390Eanj1MK6bVYJyZCtdlgBm71RsFYXt",
        'consumer_key': "xt5hvmEA7AIDd5aO90HzupgSh",
        'token_secret': "cbWvnuKJb6xyGwbC8A5DBHLv6OvV1DkAtJKBxeNDA7P9G",
        'token_key': "2841234509-FLYvS0vmnZJ98NbsMfszImH4XNCFlZ5AKRGWETK",
    }, {
        'output_file': "new_tweets_timeA.txt",
        'consumer_secret': "GEwljEljI4hiXSUdcNBcDm4He30mpDFyIDk6vEPRuOJCtbvI5P",
        'consumer_key': "23uV5qj34D4GphePcM7zpUqCy",
        'token_secret': "nHmgTX56HKaIFAKD3QQjHtbuaax0xGXOkeB32hS1XBBvy",
        'token_key': "2841234509-OvgVEOHCcSgo5cNuRBzU1wnQFR4gpzKg4PaXU6w",
    }, {
        'output_file': "new_tweets_timeB.txt",
        'consumer_secret': "ZK2MlkA7xmqCqzVxo21gXrWdl56Na6GtgFNBWdUUPWsPwAWUJU",
        'consumer_key': "TZtTf8KBUokZwqpS0y9gzm7zM",
        'token_secret': "wqbfALgDuYZixO6IwfaJZwMcIOCStg7Cl8Dg5uOyvGWd2",
        'token_key': "2841234509-8MKVhmeay4H22n5k5IQGyuqpjijlSsZzVJiqB1f",
    }, {
        'output_file': "new_tweets_timeTech.txt",
        'consumer_secret': "kZuInUJ4Z7Dsm2Bo0TZ7ZNF1LiWYxSC5yYRUgfOvetQs9OtfBK",
        'consumer_key': "Q5GsUWC2dkDpHUWZHd9PdWR4J",
        'token_secret': "uXeVYIoei51gjqZSFLwB7VDKMkwejmg3x9B5cpLH5r4mQ",
        'token_key': "2841234509-LYHFtMUMYn6McbaAUZ3osjNBv3kGOKNhzPywEsL",
    }]
    workers = Pool(len(accounts))
    res = workers.map(run, accounts)
    workers.close()
    workers.join()
    print "Exit with %s" % res.successful()
