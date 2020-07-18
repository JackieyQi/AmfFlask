#! /usr/bin/env python
# coding:utf8


class TestHandler(object):

	def get_result(self, *args, **kwargs):
		return args, kwargs
