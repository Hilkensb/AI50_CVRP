# Other Library
from redis.exceptions import ConnectionError

# Other modules
from gui.config import redis_server

def isRedisAvailable() -> bool:
    """
    """
    
    try:
        return redis_server.ping()
    except ConnectionError: 
        return False
