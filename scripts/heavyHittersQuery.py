from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator
import numpy as np
import sys
from countminsketch import HeavyHitters


def main(nh):
    conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)

    # Create a streaming context with batch interval of 60 sec
    ssc = StreamingContext(sc, 60)

    ssc.checkpoint("checkpoint")

    stopwords = load_wordlist("stop_words.txt")

    # stream for 60 seconds and receive filtered words from tweets
    Ts = stream(ssc, 60, stopwords)

    # define heavyhitters object with width and depth parameters
    hh = HeavyHitters(width=1000, depth=7, num_hitters=nh)

    #add all words to heavyhitters state object
    for word in Ts[1]:
        hh.add(word)

    #query heavy hitters
    print(hh.heavyhitters)

    #print (Ts)
    
def load_wordlist(filename):
    """
    This function should return a list or set of words from the given filename.
    """
    # YOUR CODE HERE
    file = open(filename)
    text = file.read()
    listofwords = text.split('\n')
    return listofwords


def stream(ssc, duration, stopwords):
    kstream = KafkaUtils.createDirectStream(
        ssc, topics = ['twitterstream'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})

    #get tweets and split them into words
    tweet_words = kstream.map(lambda x: x[1]).flatMap(lambda x: x.split(" "))

    #filter words and remove stopwords
    filtered_tweet_words = tweet_words.filter(lambda l: l not in stopwords)

    #list that will contain the words
    Ts = []

    #collect all filtered words
    filtered_tweet_words.foreachRDD(lambda t, rdd: Ts.append(rdd.collect()))

    #start execution
    ssc.start()
    ssc.awaitTerminationOrTimeout(duration)
    ssc.stop(stopGraceFully=True)

    #return filtered words
    return Ts


if __name__=="__main__":

    #take number of heavy hitters as input
    numHeavyHitters = int(sys.argv[1])

    main(numHeavyHitters)
