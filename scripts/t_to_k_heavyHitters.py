import json
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient
import configparser


# set appropriate keys and tokens
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


class StdOutListener(StreamListener):
    def on_data(self, data):

        try:
            producer.send_messages("twitterstream", json.loads(data)["text"].encode("utf-8"))
            print(json.loads(data)["text"].encode("utf-8"))
        except:
            pass

        return True
    def on_error(self, status):
        print (status)

# create Kafka client
kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)
l = StdOutListener()

#set authorizations
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

#track a topic, example FBI
stream.filter(languages=["en"], track=["FBI"])

