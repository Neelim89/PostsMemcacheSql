
import json
from pymemcache.client import base

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

# def getMultiplePostsFromMemcache(postIdIntArray):
#     postIdStrArr = []
#     for postIdNum : postIdIntArray:

def addPostIdToMemcache(postid):
    memcachedIds = memcacheClient.get('AllPostIds')
    if (memcachedIds is not None):
        allPostIds = json.loads(memcachedIds)
        if (allPostIds.count(postid) == 0):
            allPostIds.append(postid)
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

def getAllPostsFromMemcache():
    # First we need to get the post ids from memcache to know what
    # posts are stored in the cache
    allPosts = []
    allPostIdsMemcache = getAllPostIdsStoredInMemcache()
    for postid in allPostIdsMemcache:
        memcachedPost = getPostFromMemcache(postid)
        allPosts.append(memcachedPost)
    return allPosts

def getAllPostIdsStoredInMemcache():
    allPostIdsMemcache = []
    memcachedIds = memcacheClient.get('AllPostIds')
    if (memcachedIds is not None):
        allPostIdsMemcache = json.loads(memcachedIds)
    return allPostIdsMemcache