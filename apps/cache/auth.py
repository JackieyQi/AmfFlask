#! /usr/bin/env python
# coding:utf8

from apps.utils.common import Platform
from . import StringCache


class UserTokenCache(StringCache):
	def __init__(self, platform, user_id, is_load=False):
		key = "user_token:{user_id}:{platform}".format(
			platform=platform,
			user_id=user_id
		)
		super(UserTokenCache, self).__init__(key, is_load)

	def set_token(self, token):
		_platform = Platform()
		if _platform.is_web():
			self.save_value(token, ex=60 * 60 * 24 * 7)
		elif _platform.is_ios() or _platform.is_android():
			self.save_value(token, ex=60 * 60 * 24 * 30)
		else:
			self.save_value(token, ex=60 * 60 * 24 * 30)

	@staticmethod
	def validate_token(user_id, user_token):
		redis_client = UserTokenCache.redis
		for platform in ["web", "iOS", "Android"]:
			token = redis_client.get(
				"user_token:{user_id}:{platform}".format(user_id=user_id, platform=platform)
			)
			if token == user_token:
				return platform
		return ""

	@staticmethod
	def clear(user_id):
		for platform in ["web", "iOS", "Android"]:
			UserTokenCache(platform, user_id).delete()


class AuthTokenCache(StringCache):
	def __init__(self, token, is_load=False):
		self.token = token
		key = "auth_token:{token}".format(token=token)
		super(AuthTokenCache, self).__init__(key, is_load)

	def set_token(self, user_id):
		_platform = Platform()
		UserTokenCache(_platform.get_platform(), user_id).set_token(self.token)
		if _platform.is_web():
			self.save_value(user_id, ex=60 * 60 * 24 * 7)
		elif _platform.is_ios() or _platform.is_android():
			self.save_value(user_id, ex=60 * 60 * 24 * 30)
		else:
			self.save_value(user_id, ex=60 * 60 * 24 * 30)
