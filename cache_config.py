#redis://redis-15624.c15.us-east-1-2.ec2.redns.redis-cloud.com:15624

import os
from flask_caching import Cache

CACHE_CONFIG={
    'CACHE_TYPE':'RedisCache',
    'CACHE_REDIS_URL':os.environ.get('REDIS_URL', 'redis://localhost:6379')
}
cache=Cache(config=CACHE_CONFIG)
