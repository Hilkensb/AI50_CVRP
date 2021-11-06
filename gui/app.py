#!/usr/bin/env python3
# Standard Library
from __future__ import annotations
import os

# Other Library
from flask import Flask, render_template
from flask_sse import sse

# Other modules
from gui.config import *
from gui.mapping import *


class Application:

    def __init__(self):
        """
        """
        
        self.app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
        # Set the encryption key
        self.app.secret_key = SECRET_KEY
        # Set the redis server
        # self.app.config["REDIS_URL"] = REDIS_URL
        # Map all actions
        self.__mapActions()
        self.app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
        
    def __mapActions(self) -> None:
        """
        """
        
        # For every page mapped
        for page in mapping:
            # Mapped the function
            self.add_endpoint(page["endpoint"], page["endpoint_name"], page["action"], page["methods"])

    def add_endpoint(
        self, endpoint: str = None, endpoint_name: str = None,
        handler: function = None, methods: List = None
    ) -> None:
        """
        """

        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods)
        
    def run(
        self, host: str = HOST, port: int = PORT, debug: str = DEBUG
    ) -> None:
        """
        """

        self.app.run(host=host, port=port, debug=debug, threaded=True)


