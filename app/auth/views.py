#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'

from app import app, lm
from flask_login import current_user
from flask import redirect, request, session, g, url_for, render_template, make_response
from flask.ext.login import login_user, logout_user, current_user, login_required
from dao.models import User
import logging
from flask import jsonify
from utils.util import PublicTools
from application import python_redis_store
from application import db_manager
import random
import time


logger = logging.getLogger("login")


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.before_request
def before_request():
	if "login" not in request.full_path and "logout" not in request.full_path and "get_risk_timer" not in request.full_path and "/static/" not in request.full_path:
		g.user = current_user
		if hasattr(g.user,"username") is False:
			return render_template("login.html", params={})
		user_name = g.user.username
		recheck = python_redis_store.hget('htg_backend_login', user_name)
		if not recheck:
			return render_template("login.html", params={})
		last_login_time = int(recheck)
		cur_time = int(time.time())
		if cur_time > last_login_time + 3600:
			return render_template("login.html", params={})
		python_redis_store.hset('htg_backend_login', user_name, cur_time)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('page-404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
	return render_template('page-500.html'), 500


@app.after_request
def after_request(response):
	return response


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		password = PublicTools.md5gen(password)
		with db_manager.session_ctx(bind='backendrdb') as session:
			user = session.query(User).filter(User.username==username,User.status==1).first()
		if user is not None or user is None:
			login_user(user)
			# 用户权限放进session
			ip = request.remote_addr
			logger.info("--%s--%s---- logining" % (username, ip))
			python_redis_store.hset('htg_backend_login', username, int(time.time()))
			return redirect(url_for("index"))
		else:
			error = u"用户名或密码错误"
		info = {"username": username, "password": password}
		return render_template('login.html', error=error, params=info)
	return render_template("login.html", params={})


@app.route('/')
@app.route('/index')
@login_required
def index():
	ip = request.remote_addr

	return render_template("footer.html")


@app.route("/logout")
@login_required
def logout():
	logout_user()
	session.clear()
	return redirect(url_for("login"))


@app.route("/passwd_gen", methods=['POST'])
@login_required
def passwd_gen():
	pw_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
	           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
	           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
	           ]
	pwd = ''
	for i in range(18):
		s = random.sample(pw_list, 1)[0]
		pwd += s

	return jsonify(msg=pwd)
