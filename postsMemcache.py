
import json
from pymemcache.client import base
import time


# Setup a memcache client
memcacheClient = base.Client('localhost')

def initMemcache():
    memcacheClient.set('AllPostIds', [])

def getPostFromMemcache(postid):
    post_id_str = str(postid)
    memcachedPost = memcacheClient.get(post_id_str)
    if (memcachedPost is not None):
        post = json.loads(memcachedPost)
    else:
        post = None
    return post

def getMultiplePostsFromMemcache(postIdStrArray):
    memcachedPosts = []
    print(f'postIdStrArray: {postIdStrArray}\n')
    for postIdStr in postIdStrArray:
        memcachedPost = memcacheClient.get(postIdStr)
        if (memcachedPost is not None):
            post = json.loads(memcachedPost)
            memcachedPosts.append(post)
    return memcachedPosts

def addPostIdToMemcache(postid):
    post_id_str = str(postid)
    memcachedIds = memcacheClient.get('AllPostIds')
    if (memcachedIds is not None):
        allPostIds = json.loads(memcachedIds)
        if (allPostIds.count(post_id_str) == 0):
            allPostIds.append(post_id_str)
            memcacheClient.set('AllPostIds', json.dumps(allPostIds))

# Takes a post object and inserts it into the memcache
def setOrCreatePostInMemcache(post):
    post_id_str = str(post['id'])
    memcacheClient.set(str(post_id_str), json.dumps(post))
    # Append the key in memcache as a value to store what posts are stored
    # in the memcache
    # Store it as a string since memcache epects its
    # addPostIdToMemcache(str(post['id']))
    addPostIdToMemcache(post['id'])

def loadPostsIntoMemcache(posts):
    for post in posts:
        setOrCreatePostInMemcache(post)

def updatePostInMemcache(post_id, title, content):
    # need get the existing post from memcache since it has the other information
    # such as created date
    post = getPostFromMemcache(post_id)
    if (post is not None):
        # Update the post with the new title and content
        post['title'] = title
        post['content'] = content
        print(f'Updated post: {post}')
        # update in memcache
        setOrCreatePostInMemcache(post)

def delPostIdFromMemcache(postid):
    allPostIds = json.loads(memcacheClient.get("AllPostIds"))
    if (allPostIds.count(postid) > 0):
        allPostIds.remove(postid)
        memcacheClient.set('AllPostIds', json.dumps(allPostIds))

def deletePostInMemcache(id):
    post_id_str = str(id)
    isPostDeleteSuccess = memcacheClient.delete(post_id_str, False)
    if isPostDeleteSuccess:
        delPostIdFromMemcache(id)
    return isPostDeleteSuccess

def getAllPostIdsStoredInMemcache():
    allPostIdsMemcache = []
    startTime = time.perf_counter()
    memcachedIds = memcacheClient.get("AllPostIds")
    endTime = time.perf_counter()
    print(f'Time it took to get AllPostIds: {endTime - startTime}')
    print(f'memcachedIds: {memcachedIds}')
    if (memcachedIds is not None):
        allPostIdsMemcache = json.loads(memcachedIds)
    return allPostIdsMemcache

def getAllPostsFromMemcache():
    # First we need to get the post ids from memcache to know what
    # posts are stored in the cache
    allPosts = []
    allPostIdsMemcache = getAllPostIdsStoredInMemcache()
    startTime = time.perf_counter()
    allPosts = getMultiplePostsFromMemcache(allPostIdsMemcache)
    endTime = time.perf_counter()
    print(f'allPosts: {allPosts}')
    print(f'Time it took to getMultiplePosts: {endTime - startTime}')
    return allPosts