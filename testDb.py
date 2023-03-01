import postsSql as dbInterface
import postsMemcache as memcacheInterface
import time

dbInterface.deleteAllPostsInDb()
dbInterface.createPostInDbWithId(1, 'mypost1', 'mycontent1')
dbInterface.createPostInDbWithId(2, 'mypost2', 'mycontent2')
dbInterface.createPostInDbWithId(3, 'mypost3', 'mycontent3')
dbInterface.createPostInDbWithId(4, 'mypost4', 'mycontent4')
dbInterface.createPostInDbWithId(5, 'mypost5', 'mycontent5')
dbInterface.createPostInDbWithId(6, 'mypost6', 'mycontent6')
# # mypost = dbInterface.getPostFromDb(100)
# # print(mypost)
# allPosts = dbInterface.getAllPostsFromDb()
# dbInterface.deletePostInDb(8)
# allPosts = dbInterface.getAllPostsFromDb()
# dbInterface.updatePostInDb(12, 'mynew', 'new')
# print(allPosts)

updateSuccessful = dbInterface.updatePostInDb(5, 'newtitle!', 'newcontent!')
print(f'updateSuccessful = {updateSuccessful}\n')
allDbPosts = dbInterface.getAllPostsFromDb()
for post in allDbPosts:
    print(f'{post}\n')
print('=========================\n')
memcacheInterface.initMemcache()

memcacheInterface.loadPostsIntoMemcache(allDbPosts)
# allMemcachedPosts = memcacheInterface.getAllPostsFromMemcache()
# print('Posts retrieved from memcache:\n')
# for post in allMemcachedPosts:
#     print(f'{post}\n')
# print('=========================\n')

memcacheInterface.updatePostInMemcache(5, 'I have something to say', 'I said something')
allMemcachedPosts = memcacheInterface.getAllPostsFromMemcache()
for post in allMemcachedPosts:
    print(f'{post}\n')
print('=========================\n')

# post = memcacheInterface.getPostFromMemcache(13)
# print(f'Post: {post}\n')
# deletionSuccess = memcacheInterface.deletePostInMemcache(13)
# if (deletionSuccess):
#     print('Deletion success')
# else:
#     print('Deletion fail')
# allMemcachedPosts = memcacheInterface.getAllPostsFromMemcache()
# for post in allMemcachedPosts:
#     print(f'{post}\n')
# print('=========================\n')
# post = memcacheInterface.getPostFromMemcache(13)
# if (post is not None):
#     print(f'Post: {post}\n')
# else:
#     print(f'There is no post found with id 13\n')
deletionSuccess = memcacheInterface.deletePostInMemcache(13)
if (deletionSuccess):
    print('Deletion success, need to delete from db')
    dbInterface.deletePostInDb(13)
else:
    print('Deletion fail')


allMemcachedPosts = memcacheInterface.getAllPostsFromMemcache()
for post in allMemcachedPosts:
    print(f'{post}\n')
print('=========================\n')
postsUpdateSuccssful = dbInterface.updatePostsInDb(allMemcachedPosts)
print(f'Database update success: {postsUpdateSuccssful}')
allDbPosts = dbInterface.getAllPostsFromDb()
print(f'Posts retrieved from database:\n')
for post in allDbPosts:
    print(f'{post}\n')
print('=========================\n')
# print(f'Posts retrieved from database: {allDbPosts}\n=========================\n')

# memcacheInterface.setOrCreatePostInMemcache()

newPost = {'id' : 7, 'title' : 'mypost7', 'content' : 'mycontent7'}
startTime = time.perf_counter()
memcacheInterface.setOrCreatePostInMemcache(newPost)
endTime = time.perf_counter()
print(f'Time it took to create a post in memcache is {endTime - startTime}')

startTime = time.perf_counter()
dbInterface.createPostInDbWithId(newPost['id'], newPost['title'], newPost['content'])
endTime = time.perf_counter()
print(f'Time it took to create a post in sql database is {endTime - startTime}')

startTime = time.perf_counter()
allPosts = dbInterface.getAllPostsFromDb()
print(f'All posts from db:\n{allPosts}')
endTime = time.perf_counter()
print(f'Time it took to get all posts from database is {endTime - startTime}')

startTime = time.perf_counter()
allPosts = memcacheInterface.getAllPostsFromMemcache()
endTime = time.perf_counter()
print(f'Time it took to get all posts from memcache is {endTime - startTime}')

startTime = time.perf_counter()
memcacheInterface.getPostFromMemcache(1)
endTime = time.perf_counter()
print(f'Time it took to get post id 1 from memcache is {endTime - startTime}')

startTime = time.perf_counter()
dbInterface.getPostFromDb(1)
endTime = time.perf_counter()
print(f'Time it took to get post id 1 from database is {endTime - startTime}')