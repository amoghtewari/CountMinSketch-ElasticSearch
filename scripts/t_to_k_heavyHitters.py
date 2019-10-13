import json
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient
import configparser


# set appropriate keys and tokens
consumer_key = '3eGFm3FLrGC0C9DL1bvoNA3dp'
consumer_secret = 'FiD75AJGhV6aTancuJ86jE7FablpNaXTMJjhTkvFVjXvQXzWla'
access_token = '126882218-6iygyuYuXkrl1lWMBpCwRoe6SBTeZbjiI2hJQwJX'
access_token_secret = 'mbQbxJ8UsVURikiJUXrPiCkUfHY6kcD3a8xlCyqBUZ8Tm'
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

