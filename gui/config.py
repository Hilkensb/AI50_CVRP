# Configuration of the web application
# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union, Set
import redis as red

# ------------------------------- -------------------------------#
# Show or not solution on loading page
# If not showed it will improved time cost of the algorithms
SHOW_SOLUTION: bool = False
# Folder were all html templates are stored
TEMPLATE_FOLDER: str = "html"
# Default address
HOST: str = "localhost"
# Default port
PORT: int = 8080
# Debugging mode 
DEBUG: bool = True
# Details on the Secret Key: https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing
# the session data.
SECRET_KEY: str = 'SECRET_KEY'
# Address of the redis server
REDIS_HOST: str = "127.0.0.1"
REDIS_PORT: int = 6379
REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"

# Set the page address for the best 
SOLUTION_ADDRESS: str = "/stream"
# Topic where the solution is publish
SOLUTION_TOPIC: str = "solution_stream"
# Redis server for solution event
redis_server: red.Redis = red.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
# Session saves
instance_save: Dict = {}

