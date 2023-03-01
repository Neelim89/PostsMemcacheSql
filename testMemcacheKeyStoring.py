import json
from pymemcache.client import base
import time

# Setup a memcache client
memcacheClient = base.Client('localhost')

listNum = ["1", "2", "3", "4", "5"]

memcacheClient.set("AllPostIds", json.dumps(listNum))

startTime = time.perf_counter()
memcachedList = memcacheClient.get("AllPostIds")
endTime = time.perf_counter()
print(f'Time it took to get memcachedList from memcache: {endTime - startTime}')
print(f'memcachedList: {memcachedList}')
startTime = time.perf_counter()
memcachedList = json.loads(memcachedList)
endTime = time.perf_counter()
print(f'Time it took to json deserialize memcachedList: {endTime - startTime}')
