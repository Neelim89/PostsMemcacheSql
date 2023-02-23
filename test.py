import postsSql as dbInterface

# dbInterface.createPostInDb('mypost', 'mycontent')
# # mypost = dbInterface.getPostFromDb(100)
# # print(mypost)
# allPosts = dbInterface.getAllPostsFromDb()
# dbInterface.deletePostInDb(8)
# allPosts = dbInterface.getAllPostsFromDb()
# dbInterface.updatePostInDb(12, 'mynew', 'new')
# print(allPosts)

updateSuccessful = dbInterface.updatePostInDb(13, 'title', 'content')
updateSuccessful = dbInterface.updatePostInDb(13, 'title', 'content')
allPosts = dbInterface.getAllPostsFromDb()
print(allPosts)
print(updateSuccessful)