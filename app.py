import os

from flask import Flask
from flask_login import LoginManager

import src.config_manager as config_manager
import src.user_mgmt.datastore as datastore
from src.user_mgmt.model import UserManager


# Blueprints
import src.file_mgmt.blueprint as file_mgmt_blueprint
import src.user_mgmt.blueprint as user_mgmt_blueprint


class FileZapServer(Flask):

    def __init__(self):
        super(FileZapServer, self).__init__(__name__)
        self.secret_key = os.urandom(64)
        self._register_blueprints()
        self._init_user_manager()
        self._init_login_manager()


    def _register_blueprints(self):
        file_mgmt_blueprint.register_blueprint(self)
        user_mgmt_blueprint.register_blueprint(self)


    def _init_user_manager(self):
        config = config_manager.get_config()
        user_data_store = datastore.UserDataStore(config)
        self.user_manager = UserManager(user_data_store)
        self.user_manager.load_users()


    def _init_login_manager(self):
        login_manager = LoginManager()
        login_manager.user_callback = self.user_manager.get_user
        login_manager.init_app(self)
        login_manager.login_view = "/login"