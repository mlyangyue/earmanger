#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from application import CreateApp

# from application import CreateApp,db_manager
import pymongo

# app = CreateApp("configs.config.ProductConfig")
app = CreateApp("configs.config.TestingConfig")
mongo_url = app.config.get('MONGO_URL')
mongo_database = app.config.get('MONGO_DATEBASE')
mongo_db = pymongo.MongoClient(mongo_url)
mongo_db = mongo_db[mongo_database]

app.secret_key = "djafks#jfkda92=-("
db = SQLAlchemy(app,use_native_unicode="utf8")
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
from auth import views
from backend_users import views
from banner import views
from news import views
from news_recommend import views
from upload import views









