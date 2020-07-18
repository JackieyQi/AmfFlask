#! /usr/bin/env python
# coding:utf8

from .test import test_bp


def api_test_configure_blueprint(app):
	# app.register_blueprint(test_bp, url_prefix="/url/prefix")
	app.register_blueprint(test_bp)
