#! /usr/bin/env python
# coding:utf8

from flask import jsonify

from .resp_code import SUCCESS, FAIL, CODE_MESSAGES


def response_ok(data=None, msg=None):
	return jsonify(dict(
		code=SUCCESS,
		message=msg or CODE_MESSAGES[SUCCESS],
		data=data or {}
	))


def response_error(data=None, msg=None, code=FAIL):
	return jsonify(dict(
		code=code,
		message=msg or CODE_MESSAGES.get(code),
		data=data or {}
	))
