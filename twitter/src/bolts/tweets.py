import re
import redis

from streamparse.bolt import Bolt

class TweetBolt(Bolt):
  outputs = ["lang", "count"]
  
  def process(self, tup):
    tweet = tup.values[0]
    lang = tup.values[1]

    r_server = redis.Redis("localhost", charset="utf-8", decode_responses=True)

    if r_server.hgetall("lang"):
      if r_server.hexists("lang", lang):
        r_server.hincrby("lang", lang,  1)
      else:
        r_server.hmset("lang", {lang: 1})
    else:
      r_server.hmset("lang", {lang: 1})

    self.logger.info(lang)
    u = {}
    if lang in u.keys():
      u[lang] = u[lang]+1
    else:
      u[lang] = 1
  
    for k in u.keys():
      self.logger.info(
                "lang "+str(k)+" Count "+str(u[k])
            )
      self.emit([k, u[k]])
