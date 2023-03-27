
from pymemcache.client import base
import pickle


# Setup a memcache client
memcacheClient = base.Client('localhost')

def getPostFromMemcache(postid):
    post_id_str = str(postid)
    memcachedPost = memcacheClient.get(post_id_str)
    if (memcachedPost is not None):
        memcachedPost = pickle.loads(memcachedPost)
    return memcachedPost

# Takes a post object and inserts it into the memcache
def setPostInMemcache(post):
    post_id_str = str(post['id'])
    memcacheClient.set(post_id_str, pickle.dumps(post))

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

def deletePostInMemcache(id):
    post_id_str = str(id)
    memcacheClient.delete(post_id_str)