#! /usr/bin/env python
# coding:utf8

from functools import wraps
from flask import g, request

from apps.utils.exception import UnAuthorizationExc
from apps.models.user import db, User
from apps.cache.auth import UserTokenCache, AuthTokenCache
from apps.cache.user import UserCache


def login_required(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		auth_token = request.headers.get("AUTHORIZATION") or request.cookies.get("token")
		if not auth_token:
			raise UnAuthorizationExc()
		elif len(auth_token) != 32:
			raise UnAuthorizationExc()

		auth_token_cache = AuthTokenCache(auth_token, is_load=True)
		user_id = auth_token_cache.value
		if not user_id:
			raise UnAuthorizationExc()

		platform = UserTokenCache.validate_token(user_id, auth_token)
		if not platform:
			raise UnAuthorizationExc()

		user = User.query.filter_by(user_id=user_id).first()
		if not user:
			raise UnAuthorizationExc()

		timezone = request.headers.get("TIMEZONE")
		if timezone and str(user.timezone) != str(timezone):
			user.timezone = timezone
		if g.lang and g.lang != user.lang and request.full_path.startswith('/res/'):
			user.lang = g.lang
			UserCache(user.user_id).delete()

		db.session.commit()
		g.user = user
		return func(*args, **kwargs)
	return wrapper
