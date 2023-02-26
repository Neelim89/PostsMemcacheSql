import postsMemcache as memcacheInterface

memcacheInterface.initMemcache()

post = {'id' : 13, 'title': 'mytitle', 'content': 'mycontent'}
memcacheInterface.setOrCreatePostInMemcache(post)
allPosts = memcacheInterface.getAllPostsFromMemcache()
print(allPosts)
# print(memcacheInterface.getPostFromMemcache(13))