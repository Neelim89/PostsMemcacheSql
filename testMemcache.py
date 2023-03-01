import postsMemcache as memcacheInterface
import time

memcacheInterface.initMemcache()

post = {'id' : 1, 'title': 'mytitle', 'content': 'mycontent'}
memcacheInterface.setOrCreatePostInMemcache(post)
post = {'id' : 2, 'title': '2nd mytitle', 'content': '2nd mycontent'}
memcacheInterface.setOrCreatePostInMemcache(post)
post = {'id' : 3, 'title': '3rd mytitle', 'content': '3rd mycontent'}
memcacheInterface.setOrCreatePostInMemcache(post)
allPosts = memcacheInterface.getAllPostsFromMemcache()