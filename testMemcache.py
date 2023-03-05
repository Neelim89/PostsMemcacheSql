import postsMemcache as memcacheInterface
import time

memcacheInterface.initMemcache()

post = {'id' : 1, 'title': 'mytitle', 'content': 'mycontent'}
startTime = time.perf_counter()
memcacheInterface.setPostInMemcache(post)
endTime = time.perf_counter()
print(f'Time it took to set a post in memcache is {endTime - startTime}')

post = {'id' : 2, 'title': '2nd mytitle', 'content': '2nd mycontent'}
memcacheInterface.setPostInMemcache(post)
post = {'id' : 3, 'title': '3rd mytitle', 'content': '3rd mycontent'}
memcacheInterface.setPostInMemcache(post)
startTime = time.perf_counter()
allPosts = memcacheInterface.getAllPostsFromMemcache()
endTime = time.perf_counter()
print(f'Time it took to get all posts from memcache is {endTime - startTime}')

startTime = time.perf_counter()
allPosts = memcacheInterface.getAllPostsFromMemcache()
endTime = time.perf_counter()
print(f'Time it took to get all posts from memcache is {endTime - startTime}')

startTime = time.perf_counter()
allPosts = memcacheInterface.getAllPostsFromMemcache()
endTime = time.perf_counter()
print(f'Time it took to get all posts from memcache is {endTime - startTime}')

startTime = time.perf_counter()
allPosts = memcacheInterface.getAllPostsFromMemcache()
endTime = time.perf_counter()
print(f'Time it took to get all posts from memcache is {endTime - startTime}')

memcacheInterface.addPostIdToMemcache(1)
memcacheInterface.addPostIdToMemcache(2)
memcacheInterface.addPostIdToMemcache(3)
allPostIds = memcacheInterface.getAllPostIdsStoredInMemcache()
print(f'allPostIds is {allPostIds}\n')
# memcacheInterface.memcacheClient.add("AllPostIds")