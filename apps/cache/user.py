#! /usr/bin/env python
# coding:utf8

from . import StringCache


class UserCache(StringCache):
	def __init__(self, user_id, is_load=False):
		self.user_id = user_id
		key = "user:{user_id}".format(user_id=user_id)
		super(UserCache, self).__init__(key, is_load)
