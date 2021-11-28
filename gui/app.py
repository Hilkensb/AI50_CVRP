#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
import os
from sys import platform
import subprocess

# Other Library
from flask import Flask, render_template
from flask_sse import sse
# To color text in terminal
from colorama import Fore, Back, Style

# Other modules
from gui.config import *
from gui.mapping import *
from utils.redisutils import isRedisAvailable


class Application:

    def __init__(self):
        """
        Constructor
        """
        
        # Set the flask environement to developement
        # HARD CODE since default is production
        os.environ['FLASK_ENV'] = 'development'
        
        self.app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
        # Set the encryption key
        self.app.secret_key = SECRET_KEY
        # Set the redis server
        # self.app.config["REDIS_URL"] = REDIS_URL
        # Map all actions
        self.__mapActions()
        self.app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
        # Set the folder where the pdf will be stored
        self.app.config["CLIENT_PDF"] = os.path.join(os.getcwd(), PDF_FOLDER)
        
    def __del__(self):
        """
        Destructor. It used to stop the sarl application
        """
        
        # Send a stop on sarl topic if needed
        if STOP_JAVA and isRedisAvailable():
            # Publish stop on sarlTopic to tell the sarl agent to kill it self
            redis_server.publish("sarlTopic", "stop")
            
        # Call the super destructor if there's one
        super()
        
    def __mapActions(self) -> None:
        """
        __mapActions()
        
        Method to map all the actions (controller) recorded in the mapping
        """
        
        # For every page mapped
        for page in mapping:
            # Mapped the function
            self.addEndpoint(page["endpoint"], page["endpoint_name"], page["action"], page["methods"])

    def addEndpoint(
        self, endpoint: str = None, endpoint_name: str = None,
        handler: function = None, methods: List[str] = None
    ) -> None:
        """
        addEndpoint()
        
        Method to add an endpoint (link a controller to an url)

        :param endpoint: url for the mapping. Default to None (opt.)
        :type endpoint: str
        :param endpoint_name: Name of the point to then retrieve the url and/or the controller. Default to None (opt.)
        :type endpoint_name: str
        :param handler: Function tha will be called when the user will go on the end point. Default to None (opt.)
        :type handler: function
        :param methods: Type of actions (\"POST\", \"GET\"). Default to None (opt.)
        :type methods: List[str]
        """

        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods)
        
    def run(
        self, host: str = HOST, port: int = PORT, debug: str = DEBUG
    ) -> None:
        """
        run()
        
        Method to launch the web application
        
        :param host: Address hosting the web application, default to HOST value (opt.)
        :type host: str
        :param port: Port of the address hosting the web application, default to PORT value (opt.)
        :type host: int
        :param debug: True if the server should be in debug mode, default to DEBUG value (opt.)
        :type debug: bool
        """

        # Check if redis is available
        if not isRedisAvailable():
            # Display a warning message
            print(Fore.YELLOW + "/!\ WARNING: Redis server is not available for the application. Some functionnalities will not work." + Style.RESET_ALL)
            
            # If we should launch redis 
            if AUTO_LAUNCH_REDIS:
                # Check the os
                # If it's windows
                if platform == "win32":
                    # Run redis server
                    subprocess.Popen(os.path.join(WINDOWS_REDIS_FOLDER, "redis-server.exe"))
                    print(Fore.GREEN + "Redis has been launched." + Style.RESET_ALL)
                else:
                   print(Fore.YELLOW + "/!\ WARNING: Functionnality unavailable for your os. You need to launch redis manually." + Style.RESET_ALL)

        self.app.run(host=host, port=port, debug=debug, threaded=True)

