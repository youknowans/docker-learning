# app.py

from flask import Flask
import redis
import os

app = Flask(__name__)
# Connect to the Redis database

r = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'redis'),
    port=os.environ.get('REDIS_PORT', 6379),
    db=0
)

@app.route('/')
def welcome():
    return f'Welcome to the Flask App!'

@app.route('/count')
def counter():
     # Increment a counter in Redis
    count = r.incr("counter")
    return f'Visit count: {count}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)