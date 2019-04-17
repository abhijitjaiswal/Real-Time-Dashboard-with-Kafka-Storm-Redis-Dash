from streamparse.spout import Spout
from kafka import KafkaConsumer
from json import loads

class TweetSpout(Spout):
  outputs=["tweet", "lang"]
  
  def initialize(self, stormconf, context):
    self.consumer = KafkaConsumer("test", bootstrap_servers=['localhost:9092'], 
			auto_offset_reset='earliest', value_deserializer = lambda x: loads(x.decode('utf-8')) )
    
  def next_tuple(self):
    for msg in self.consumer:
      self.logger.info(msg.value["lang"])
      self.emit([msg.value["text"], msg.value["lang"]])
