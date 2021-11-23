# Configuration of the web application
# Standard Library
from __future__ import annotations
from typing import List, Dict, Tuple, Union, Set
import redis as red

# -------------------------------- Parameters --------------------------------#
# __________________________ Application Parameter __________________________ #

# Show or not solution on loading page
# If not showed it will improved time cost of the algorithms
SHOW_SOLUTION: bool = False

# _____________________________ Flask Parameter _____________________________ #

# ~~~~~~~~~~~~~~~~~~~~~~~~~~  Flask Folder setting ~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# Folder were all html templates are stored
TEMPLATE_FOLDER: str = "html"
# Folder were pdf are stored
PDF_FOLDER: str = "gui\static\pdf\\"

# ~~~~~~~~~~~~~~~~~~~~~~~~~  Flask Address settings ~~~~~~~~~~~~~~~~~~~~~~~~~ #

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

# Set the page address for the best 
SOLUTION_ADDRESS: str = "/stream"
# Topic where the solution is publish
SOLUTION_TOPIC: str = "solution_stream"
# Topic where the sarl final solution is publish
SARL_SOLUTION_TOPIC: str = "sarl_final_solution"

# ~~~~~~~~~~~~~~~~~~~~~~~~~  Maps Address settings ~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# /!\ Works only with plotly graph /!\
# The Latitude and longitude of UTBM
# DEFAULT_LATITUDE: float = 47.641601
# DEFAULT_LONGITUDE: float = 6.844548
# Default latitude for the map
DEFAULT_LATITUDE: float = 47.641601
# Default longitude for the map
DEFAULT_LONGITUDE: float = 6.844548
# The add to latitude and longitude per units
UNITS_MAP: float = 0.005
# Bool to know if we use maps by default or graph representation
# True for maps
# False for graph
MAPS_REPRESENTATION: bool = True

# --------------------- Param that should not be changed -------------------- #
# _____________________________ Redis Parameter _____________________________ #

# Address of the redis server
REDIS_HOST: str = "127.0.0.1"
REDIS_PORT: int = 6379
REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"
# Redis server for solution event
redis_server: red.Redis = red.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
# Session saves
instance_save: Dict = {}

