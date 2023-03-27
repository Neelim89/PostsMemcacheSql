import sqlite3
from pymemcache.client import base
conn = sqlite3.connect('database.db')
conn.execute('DELETE FROM posts')
conn.commit()
conn.close()

memcacheClient = base.Client('localhost')
memcacheClient.flush_all()