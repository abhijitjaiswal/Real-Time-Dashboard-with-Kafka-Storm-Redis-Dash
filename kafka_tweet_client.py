from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient

# Put the token below and uncomment following code.

#access_token = "(get your own)"
#access_token_secret =  "(get your own)"
#consumer_key =  "(get your own)"
#consumer_secret =  "(get your own)"

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_key, access_secret)

class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages("test", data.encode('utf-8'))
        #print (data)
        return True
    def on_error(self, status):
        print (status)

kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)
l = StdOutListener()
#auth = OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.filter(track=["cricket"])
