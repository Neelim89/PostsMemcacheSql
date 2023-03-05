
from pymemcache.client import base
import pickle


# Setup a memcache client
memcacheClient = base.Client('localhost')

def initMemcache():
    memcacheClient.flush_all()
    memcacheClient.set('AllPostIds', pickle.dumps([]))

def getPostFromMemcache(postid):
    post_id_str = str(postid)
    memcachedPost = memcacheClient.get(post_id_str)
    if (memcachedPost is not None):
        post = pickle.loads(memcachedPost)
    else:
        post = None
    return post

def getMultiplePostsFromMemcache(postIdStrArray):
    memcachedPosts = []
    postDict = memcacheClient.get_multi(postIdStrArray)
    for memcachedPost in postDict.values():
        if (memcachedPost is not None):
            post = pickle.loads(memcachedPost)
            memcachedPosts.append(post)
    return memcachedPosts

def addPostIdToMemcache(postid):
    post_id_str = str(postid)
    memcachedIds = memcacheClient.get('AllPostIds')
    if (memcachedIds is not None):
        allPostIds = pickle.loads(memcachedIds)
        if (allPostIds.count(post_id_str) == 0):
            allPostIds.append(post_id_str)
            # Must sort the list for other operations
            allPostIds.sort()
            memcacheClient.set('AllPostIds', pickle.dumps(allPostIds))

# Takes a post object and inserts it into the memcache
def setPostInMemcache(post):
    post_id_str = str(post['id'])
    memcacheClient.set(str(post_id_str), pickle.dumps(post))
    addPostIdToMemcache(post['id'])

# Creates a new post in memcache with the given title and content,
# and automatically assigns a new post id which will be the
# id of the post with the greatest post id plus 1
def createNewPostInMemcache(title, content):
    # look for the greatest post id stored in the cache and create
    # a new id using the currently greatest id plus 1
    allPostIds = getAllPostIdsStoredInMemcache()
    # This list is sorted, so the last element is the largest
    largestPostId = allPostIds[len(allPostIds) - 1]
    newPostId = int(largestPostId) + 1
    newPost = {'id': newPostId, 'title': title, 'content': content}
    setPostInMemcache(newPost)

def loadPostsIntoMemcache(posts):
    for post in posts:
        setPostInMemcache(post)

def updatePostInMemcache(post_id, title, content):
    # need get the existing post from memcache since it has the other information
    # such as created date
    post = getPostFromMemcache(post_id)
    if (post is not None):
        # Update the post with the new title and content
        post['title'] = title
        post['content'] = content
        # update in memcache
        setPostInMemcache(post)

def delPostIdFromMemcache(postid):
    allPostIds = pickle.loads(memcacheClient.get("AllPostIds"))
    if (allPostIds.count(postid) > 0):
        allPostIds.remove(postid)
        memcacheClient.set('AllPostIds', pickle.dumps(allPostIds))

def deletePostInMemcache(id):
    post_id_str = str(id)
    isPostDeleteSuccess = memcacheClient.delete(post_id_str, False)
    if isPostDeleteSuccess:
        delPostIdFromMemcache(id)
    return isPostDeleteSuccess

def getAllPostIdsStoredInMemcache():
    allPostIdsMemcache = []
    memcachedIds = memcacheClient.get("AllPostIds")
    if (memcachedIds is not None):
        allPostIdsMemcache = pickle.loads(memcachedIds)
    return allPostIdsMemcache

def getAllPostsFromMemcache():
    # First we need to get the post ids from memcache to know what
    # posts are stored in the cache
    allPosts = []
    allPostIdsMemcache = getAllPostIdsStoredInMemcache()
    allPosts = getMultiplePostsFromMemcache(allPostIdsMemcache)
    return allPosts