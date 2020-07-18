#! /usr/bin/env python
# coding:utf8

import os
import logging
import traceback
from flask import (
	Flask, g, request, session, jsonify, make_response, render_template, render_template, current_app
)

from apps.ext import csrf, db, celery
from apps.utils.xhr import response_error
from apps.utils.exception import StandardResponseExc


def create_app(*args, **kwargs):
	app = Flask(__name__)
	app.config.from_pyfile("setting/default.py")
	if os.path.exists(os.path.join(app.root_path, "setting/dev.py")):
		app.config.from_pyfile("setting/dev.py")
	if os.path.exists(os.path.join(app.root_path, "setting/test.py")):
		app.config.from_pyfile("setting/test.py")
	if os.path.exists(os.path.join(app.root_path, "settings/prod.py")):
		app.config.from_pyfile("setting/prod.py")

	init_configure_blueprint(app)
	init_configure_logging(app)
	init_configure_extension(app)
	init_configure_handler(app)
	init_configure_jinja(app)
	return app


def init_configure_blueprint(app):
	from apps.api_test import api_test_configure_blueprint
	api_test_configure_blueprint(app)


def init_configure_logging(app):
	app.logger.setLevel(logging.INFO)
	# app.logger.addHandler(log_handler)


def init_configure_extension(app):
	csrf.init_app(app)
	db.init_app(app)
	celery.conf.update(app.config)

	class ContextTask(celery.Task):
		def on_failure(self, exc, task_id, args, kwargs, einfo):
			if isinstance(exc, StandardResponseExc):
				return

			err_str = traceback.format_exc()
			with app.app_context():
				if not current_app.config.get("EXCEPTION_CELERY_ALERT"):
					return

				task_info_str = "task_name:{}, args:{}, kwargs:{}".format(self.name, args, kwargs)
				err_str = "\n".join([task_info_str, err_str])
				current_app.logger.error(err_str)
			# send_notice_task.delay(err_str.replace("\n", "<br>"))

	celery.Task = ContextTask


def init_configure_handler(app):
	@app.before_request
	def before_request():
		csrf.protect()

	@app.errorhandler(Exception)
	@app.errorhandler(StandardResponseExc)
	def error_handler(error):
		return response_error(error.data, error.message, error.code)


def init_configure_jinja(app):
	app.jinja_env.globals["int"] = int
