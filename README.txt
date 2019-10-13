python : Python 2.7.12
================================================================
Submission file: submission.zip

unzip the submission.zip file
================================================================
Folders in submission folder:
scripts
config
================================================================
There will be 5 python scripts and 1 .txt file in script folder
twitter_to_kafka.py
queriestest.py
countminsketch.py
t_to_k_heavyHitters.py
heavyHittersQuery.py
stop_words.txt
===============================================================
There will be 2(.properties) config files in config folder
connect-standalone.properties
elasticsearch-connect.properties



===============================================================
Commands for Elasticseach Execution(Part A and B)
===============================================================
Run Zookeeper
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties

Run Kafka
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties

Create topic name twitterstream
$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic twitterstream

Follow Documentation folder for Elasticsearch setup

Create Index in Elasticsearch
curl -X PUT "localhost:9200/twitterstream"

Install Tweepy
sudo pip install tweepy

Run the Kafka Connector
cd $KAFKA_HOME
bin/connect-standalone.sh config/connect-standalone.properties config/elasticsearch-connect.properties
================================================================
Scripts Execution
================================================================
twitter_to_kafka.py : To stream tweets execute 

Usage:
python twitter_to_kafka.py

queriestest.py : To test DRPC queries
Usage:
python queriestest.py
===========================================================


===============================================================
Commands for CountMinSketch and HeavyHitters(Part A and B)
===============================================================
Run Zookeeper
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties

Run Kafka
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties

Create topic name twitterstream
$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic twitterstream


================================================================
Scripts Execution
================================================================
t_to_k_heavyHitters.py : To stream tweets execute 

Usage:
python python t_to_k_heavyHitters.py

heavyHittersQuery.py : To find heavy hitters
Usage:
$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 heavyHittersQuery.py k

where k is the number of heavy hitters, example for 10 heavy hitter outputs;
$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 heavyHittersQuery.py 10


===========================================================
