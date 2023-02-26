# You first import the sqlite3 module to use it to connect to your database.
# Then you import the Flask class and the render_template() function from the
# flask package. You make a Flask application instance called app.

from flask import Flask, render_template, request, url_for, flash, redirect
import pdb

import postsSql as dbInterface
import postsMemcache as memcacheInterface

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def storeCacheToDb():
    allCachedPosts = memcacheInterface.getAllPostsFromMemcache()
    dbInterface.updatePostsInDb(allCachedPosts)

def loadDbToCache():
    allStoredPosts = dbInterface.getAllPostsFromDb()
    memcacheInterface.loadPostsIntoMemcache(allStoredPosts)

def startup():
    loadDbToCache()

startup()

# You use the route /<int:id>/edit/, with int: being a converter that accepts positive integers.
# And id is the URL variable that will determine the post you want to edit. For example,
# /2/edit/ will allow you to edit the post with the ID of 2. The ID is passed from the URL
# to the edit() view function. You pass the value of the id argument to the get_post() function
# to fetch the post associated with the provided ID from the database. Remember that this will
# respond with a 404 Not Found error if no post with the given ID exists.
# The last line renders a template file called edit.html, and passes in the post variable that
# has the post data. You’ll use this to display the existing title and content on the Edit page.
# The if request.method == 'POST' block handles the new data the user submits. Similar to adding
# a new post, you extract the title and content. You flash a message if the title or the content
# is not provided.

# If the form is valid, you open a database connection and use the UPDATE SQL statement to update the posts table by setting the new title and new content, where the ID of the post in the database is equal to the ID that was in the URL. You commit the transaction, close the connection, and redirect to the index page.
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            # Update the SQL database
            update_post_in_db(id, title, content)
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

# In this route, you pass the tuple ('GET', 'POST') to the methods parameter to allow both GET
# and POST requests. GET requests are used to retrieve data from the server. POST requests are
# used to post data to a specific route. By default, only GET requests are allowed. When the user
# first requests the /create route using a GET request, a template file called create.html will be
# rendered.
# You handle POST requests inside the if request.method == 'POST' condition. You extract the title
# and content the user submits from the request.form object. If the title is empty, you use the
# flash() function to flash the message Title is required!. You do the same in case of empty content.
# If both the title and the content are supplied, you open a database connection using the
# get_db_connection() function. You use the execute() method to execute an INSERT INTO SQL statement
# to add a new post to the posts table with the title and content the user submits as values.
# You use the ? placeholder to insert data into the table safely. You commit the transaction and
# close the connection. Lastly, you redirect the user to the index page where they can see their
# new post below existing posts.
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            create_post_in_db(title, content)
            return redirect(url_for('index'))

    return render_template('create.html')

# This view function only accepts POST requests in the methods parameter. This means that
# navigating to the /ID/delete route on your browser will return a 405 Method Not Allowed
# error, because web browsers default to GET requests. To delete a post, the user clicks
# on a button that sends a POST request to this route.
# The function receives the ID of the post to be deleted. You use this ID to retrieve
# the post using the get_post() function. This responds with a 404 Not Found error if
# no post with the given ID exists. You open a database connection and execute a DELETE
# FROM SQL command to delete the post. You use WHERE id = ? to specify the post you want
# to delete.
# You commit the change to the database and close the connection. You flash a message to
# inform the user that the post was successfully deleted and redirect them to the index page.
# Note that you don’t render a template file. This is because you’ll just add a Delete button
# to the Edit page.
@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = memcacheInterface.deletePostInMemcache(id)
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

# You then use the app.route() decorator to create a Flask view function called index().
# You use the get_db_connection() function to open a database connection. Then you execute
# an SQL query to select all entries from the posts table. You use the fetchall() method to
# fetch all the rows of the query result, this will return a list of the posts you inserted
# into the database in the previous step.
# You close the database connection using the close() method and return the result of
# rendering the index.html template. You also pass the posts object as an argument,
# which contains the results you got from the database. This will allow you to access
# the blog posts in the index.html template.
@app.route('/')
def index():
    # get the posts from memcache
    posts = memcacheInterface.getAllPostsFromMemcache()

    return render_template('index.html', posts=posts)