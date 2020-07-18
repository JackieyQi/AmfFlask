#! /usr/bin/env python
# coding:utf8

import hashlib
from uuid import uuid4
from datetime import datetime
from flask import request


class Platform(object):
	IOS = "iOS"
	ANDROID = "Android"
	WEB = "web"

	def __init__(self):
		self._platform = self.get_platform()

	def is_ios(self):
		return self._platform == self.IOS

	def is_android(self):
		return self._platform == self.ANDROID

	def is_web(self):
		return self._platform == self.WEB

	@staticmethod
	def get_platform():
		return request.headers.get("PLATFORM", "unknown")

	@classmethod
	def get_build_version(cls):
		return request.headers.get("BUILD", "0")


def generate_token(random_string, length=32):
	return (uuid4().hex + hashlib.sha256((str(datetime.now()) + str(random_string)).encode("utf8")).hexdigest())[:length].upper()
