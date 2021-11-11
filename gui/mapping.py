# Standard Library
from __future__ import annotations

# Other modules
from gui.controller import *
from gui.config import *


mapping: List = [
    {
        "endpoint": "/", 
        "endpoint_name": "index",
        "action": index, 
        "methods": None
    },
    {
        "endpoint": "/algorithm/<instance_type>/<cvrp_id>/", 
        "endpoint_name": "readInstance",
        "action": readInstance, 
        "methods": ['GET', 'POST']
    },
    {
        "endpoint": f"/stream/<cvrp_id>/", 
        "endpoint_name": "stream",
        "action": stream, 
        "methods": None
    },
    {
        "endpoint": "/load/<cvrp_id>/", 
        "endpoint_name": "load",
        "action": load, 
        "methods": ['GET', 'POST']
    },
    {
        "endpoint": "/result/<cvrp_id>/", 
        "endpoint_name": "result",
        "action": result, 
        "methods": None
    },
    {
        "endpoint": "/download/<cvrp_id>/", 
        "endpoint_name": "downloadFile",
        "action": downloadFile, 
        "methods": None
    }
]
