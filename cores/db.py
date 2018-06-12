#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
import random
from cores.webpydb import database


class DB(object):
    def __init__(self, app=None, **connect_kwargs):
        """

        :param user:
        :param password:
        :param database:
        :param host:
        :param port:
        :param connect_kwargs:
        :return:
        """
        self.app = app
        self.master = None
        self.master_other = None
        self.slave = None
        self.db_config = connect_kwargs.get("db_config", "")
        print  self.db_config
        self.__master_dburl = None
        self.__master_other_dburl = None
        self.__slave_dburls = None
        if self.db_config:
            self.__master_dburl = self.db_config["master"]
            self.__master_other_dburl = self.db_config["master_other"]
            self.__slave_dburls = self.db_config.get("slave", [])

        if self.app:
            self.init_app(self.app)

    def init_app(self, app, **connect_kwargs):
        self.db_config = app.config.get("DB")
        self.__master_dburl = self.db_config["master"]
        self.__master_other_dburl = self.db_config["master_other"]
        self.__slave_dburls = self.db_config.get("slave", [])
        self.init_master()
        self.init_master_other()
        self.init_slave()

    def init_master(self):
        self.master = database(dburl=self.__master_dburl,aotucommit=False)
    def init_master_other(self):
        self.master_other = database(dburl=self.__master_other_dburl, aotucommit=False)

    def init_slave(self):
        slave_count = len(self.__slave_dburls)
        if slave_count == 0:
            if self.master:
                self.slave = self.master
                return
            dburl = self.__master_dburl
        else:
            dburl = self.__slave_dburls[random.randint(0, slave_count - 1)]

        self.slave = database(dburl=dburl)


