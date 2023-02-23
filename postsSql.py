import sqlite3

# This dict_factory defines how to return the SQL queries
# as a dictionary representing the data where the keys are the
# columns and the values are the associated rows
def dictFactory(cursor, row):
    # get the column names from the table to be used as the
    # key in the dictionary
    fields = [column[0] for column in cursor.description]
    # make a dictionary using the first column, which is
    # the name of the value stored in the table
    # This is done by using the zip function which
    # creates a dictionary from the fields and row,
    # where fields is the column name and row is the actual
    # value; this is done for all entries in the dictionary
    return {key: value for key, value in zip(fields, row)}

# You define a function called get_db_connection(), which opens a connection to the database.db
# database file you created earlier, and sets the row_factory attribute to sqlite3.Row
# so you can have name-based access to columns. This means that the database connection
# will return rows that behave like regular Python dictionaries. Lastly, the function
# returns the conn connection object you’ll be using to access the database.
def getDbConnection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dictFactory
    return conn

def createPostInDb(title, content):
    createSuccessful = False
    conn = getDbConnection()
    cursor = conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                    (title, content))
    conn.commit()
    conn.close()
    if (cursor.rowcount == 1):
        createSuccessful = True

    return createSuccessful

def updatePostInDb(post_id, title, content):
    updateSuccessful = False
    conn = getDbConnection()
    cursor = conn.execute('UPDATE posts SET title = ?, content = ?'
                ' WHERE id = ?',
                (title, content, post_id))
    conn.commit()
    conn.close()
    if (cursor.rowcount == 1):
        updateSuccessful = True

    return updateSuccessful

# This function has a post_id argument that determines what post to retrieve and return.
# You open a database connection with get_db_connection() and execute an SQL query to get the
# post associated with the given post_id value. You get the post with the fetchone() method,
# store it in the post variable, and close the connection.
def getPostFromDb(post_id):
    # if memcache returns null, that is, there are no posts cached, then look in the SQL database
    # and then store in memcache
    conn = getDbConnection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                    (post_id,)).fetchone()
    conn.close()
    return post

def deletePostInDb(post_id):
    conn = getDbConnection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()

def getAllPostsFromDb():
    conn = getDbConnection()
    posts = conn.execute('SELECT * FROM posts',).fetchall()
    conn.close()
    return posts

def updatePostsInDb(posts):
    for post in posts:
        updatePostInDb(post['id'], post['title'], post['content'])