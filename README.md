# Real Time Dashboard for Tweet Languages Count for Topic "Cricket"

This project creates a real time dashboard for Tweet's languages.

## Requirements:
1. Python 3.7 (preferrably)
   Install following libraries:
   "pip install Tweepy", 
   "pip install Dash",
   "pip install pykafka"
2. Apache Kafka: kafka_2.12-2.2.0 or above (get it from https://kafka.apache.org/downloads)
3. Apache Storm: apache-storm-1.2.2 ( get it from https://storm.apache.org/downloads.html)
4. Streamparse: (This is a python library for Storm, Quickstart guide https://streamparse.readthedocs.io/en/v2.1.0/quickstart.html)
5. Redis: Redis is an in-memory Data Structure Store used as a DB. (Get it from https://redis.io/)
6. Dash: (This is Python Library to visualize Dashboard on web app, Getting Started https://dash.plot.ly/)

## Steps
Once all the things are installed or downloaded.

1. Go to Kafka Folder and start zookeeper service:
	./bin/zookeeper-server-start.sh config/zookeeper.properties 

2. From the same folder start Kafka server:
	./bin/kafka-server-start.sh config/server.properties 

3. Now let's create a Topic "test" in Kafka (the topic name can be changed but you will need to change it in the python files as well):
	./bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test

4. Update the Twitter keys in kafka_tweet_client.py file. And run the file using "python kafka_tweet_client.py", this will run forever untill stopped and start populating the topic "test" with the tweets.

5. Add the storm bin path to $PATH so that "storm" is accessible to streamparse.
	export PATH=$PATH:<STORM_HOME>/apache-storm-1.2.2/bin/

6. Start Redis Server. This tutorial will help: https://www.youtube.com/watch?v=CkwJjN0JhHo

7. Go to "Twitter" folder from the project and exeucte "sparse run". This will start the storm job and process the incoming tweets and push them into Redis "lang" hashset.This can be seen in redis by running following command 
	"hgetall lang"

8. Check if the redis server has the hashset "lang" to be on safer side (A check needs to be added in the app_redis.py for this, currently it will throw an exception).

9. Once the redis server has the hashset, run the "app_redis.py" using "python app_redis.py" command and navigate to "http://127.0.0.1:8050/" on your web browser. You should see the following graph which keeps on updating every 5 seconds.

![alt text](images/chart.png?raw=true "Title")

###  Note: This is still work in progress, please let me know for issues.
