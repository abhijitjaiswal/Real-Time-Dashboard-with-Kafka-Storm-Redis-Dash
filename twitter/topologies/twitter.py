
from streamparse import Grouping, Topology

from bolts.tweets import TweetBolt
from spouts.tweets import TweetSpout

class Twitter(Topology):

  tweet_spout = TweetSpout.spec()
  tweet_bolt = TweetBolt.spec(inputs={tweet_spout: Grouping.fields("lang")}, par=2)
