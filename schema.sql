-- In this schema file, you first delete the posts table if it already exists.
-- This avoids the possibility of another table named posts existing, which might
-- result in confusing behavior (for example, if it has different columns).
-- This isn’t the case here, because you haven’t created the table yet, so the SQL
-- command won’t be executed. Note that this will delete all of the existing data whenever
-- you execute this schema file. For our purposes, you will only execute this schema once,
-- but you might want to execute it again to delete whatever data you inserted and start
-- with an empty database again.

DROP TABLE IF EXISTS posts;

-- Next, you use CREATE TABLE posts to create the posts table with the following columns:
-- id:      An integer that represents a primary key. This key will get assigned a unique value
--          by the database for each entry (that is, each blog post). AUTOINCREMENT automatically
--          increments the post IDs, so that the first post will have an ID of 1, and the post added
--          after it will have an ID of 2, and so on. Each post will always have the same ID, even
--          if other posts are deleted.
-- created: The time the blog post was created. NOT NULL signifies that this column should
--          not be empty, and the DEFAULT value is the CURRENT_TIMESTAMP value, which is the time at
--          which the post was added to the database. Just like id, you don’t need to specify a value
--          for this column, as it will be automatically filled in.
-- title:   The post title. NOT NULL signifies that this column can’t be empty.
-- content: The post content. NOT NULL signifies that this column can’t be empty.

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);