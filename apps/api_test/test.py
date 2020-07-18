#! /usr/bin/env python
# coding:utf8

from flask import Blueprint, g
from flask_restful import Api, marshal, Resource, fields, reqparse

from apps.utils.xhr import response_ok, response_error
from apps.auth import login_required

from business.test import TestHandler

test_bp = Blueprint("test", __name__)
test_api = Api(test_bp)


class TestApi(Resource):
	base_fields = {
		"test_ts": fields.Integer,
	}

	base_get_parse = reqparse.RequestParser()
	base_get_parse.add_argument("test", type=str, default="")

	@login_required
	def get(self):
		args = self.base_get_parse.parse_args()
		return response_ok(data=TestHandler().get_result(*args))


test_api.add_resource(TestApi, "/api/test/")
