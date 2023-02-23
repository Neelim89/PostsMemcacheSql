
import json
from pymemcache.client import base
import postsSql as dbInterface
from enum import Enum

# Setup a memcache client
memcacheClient = base.Client('localhost')

def addPostIdToMemcache(postid):
    allPostIds = memcacheClient.get("AllPostIds")
    if (allPostIds.get(postid) is None):
        allPostIds.append(postid)
    memcacheClient.set("AllPostIds", allPostIds)

def delPostIdFromMemcache(postid):
    allPostIds = memcacheClient.get("AllPostIds")
    if (allPostIds.get(postid) is not None):
        allPostIds.remove(postid)
    memcacheClient.set("AllPostIds", allPostIds)

def getPostFromMemcache(post):
    post_id_str = str(post['id'])
    memcachedPost = memcacheClient.get(post_id_str)
    post = json.loads(memcachedPost.decode("utf-8"))
    return post

def setOrCreatePostInMemcache(post):
    post_id_str = str(post['id'])
    memcachedPost = memcacheClient.set(str(post_id_str), json.dumps(post))
    # Append the key in memcache as a value to store what posts are stored
    # in the memcache
    addPostIdToMemcache(post_id_str)

def loadPostsIntoMemcache(posts):
    for post in posts:
        setOrCreatePostInMemcache(post)

def updatePostInMemcache(post_id, title, content):
    # need get the existing post from memcache since it has the other information
    # such as created date
    post = getPostFromMemcache(post_id)
    # Update the post with the new title and content
    post['title'] = title
    post['content'] = content
    # update in memcache
    setOrCreatePostInMemcache(post)

def deletePostInMemcacheUsingPostObj(post):
    post_id_str = str(post['id'])
    memcacheClient.delete(post_id_str)
    delPostIdFromMemcache(post['id'])

def getAllPostsFromMemcache():
    # First we need to get the post ids from memcache to know what
    # posts are stored in the cache
    allPosts = []
    allPostIds = memcacheClient.get("AllPostIds")
    for postid in allPostIds:
        memcachedPost = memcacheClient.get(postid)
        allPosts.append(memcachedPost)
    return allPosts