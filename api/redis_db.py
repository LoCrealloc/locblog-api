from redis import Redis

from api.config import redis_host, redis_port, redis_db

rds = Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
