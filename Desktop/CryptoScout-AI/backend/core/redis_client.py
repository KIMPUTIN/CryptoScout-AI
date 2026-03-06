
import redis
import os
import json

REDIS_URL = os.getenv("REDIS_URL")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)


def cache_get(key):
    value = redis_client.get(key)
    if value:
        import json
        return json.loads(value)
    return None


def cache_set(key, value, ttl):
    import json
    redis_client.setex(key, ttl, json.dumps(value))