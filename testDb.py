import postsSql as dbInterface
import postsMemcache as memcacheInterface

# dbInterface.createPostInDb('mypost', 'mycontent')
# # mypost = dbInterface.getPostFromDb(100)
# # print(mypost)
# allPosts = dbInterface.getAllPostsFromDb()
# dbInterface.deletePostInDb(8)
# allPosts = dbInterface.getAllPostsFromDb()
# dbInterface.updatePostInDb(12, 'mynew', 'new')
# print(allPosts)

updateSuccessful = dbInterface.updatePostInDb(13, 'title', 'content')
allDbPosts = dbInterface.getAllPostsFromDb()
memcacheInterface.initMemcache()

memcacheInterface.loadPostsIntoMemcache(allDbPosts)
allMemcachedPosts = memcacheInterface.getAllPostsFromMemcache()
print('Posts retrieved from memcache:\n')
for post in allMemcachedPosts:
    print(f'{post}\n')
print('=========================\n')

memcacheInterface.updatePostInMemcache(13, 'I have something to say', 'I said something')
allMemcachedPosts = memcacheInterface.getAllPostsFromMemcache()
for post in allMemcachedPosts:
    print(f'{post}\n')
print('=========================\n')

post = memcacheInterface.getPostFromMemcache(13)
print(f'Post: {post}\n')
deletionSuccess = memcacheInterface.deletePostInMemcache(13)
if (deletionSuccess):
    print('Deletion success')
else:
    print('Deletion fail')
allMemcachedPosts = memcacheInterface.getAllPostsFromMemcache()
for post in allMemcachedPosts:
    print(f'{post}\n')
print('=========================\n')
post = memcacheInterface.getPostFromMemcache(13)
if (post is not None):
    print(f'Post: {post}\n')
else:
    print(f'There is no post found with id 13\n')
deletionSuccess = memcacheInterface.deletePostInMemcache(13)
if (deletionSuccess):
    print('Deletion success')
else:
    print('Deletion fail')


# allMemcachedPosts = memcacheInterface.getAllPostsFromMemcache()
# dbInterface.updatePostsInDb(allMemcachedPosts)
# allDbPosts = dbInterface.getAllPostsFromDb()
# print(f'Posts retrieved from database: {allDbPosts}\n=========================\n')