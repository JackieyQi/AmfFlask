#! /usr/bin/env python
# ! coding:utf8

import time
from flask import current_app
from redis import StrictRedis

redis_conn = None


class RedisCfgMixin(object):
	@property
	def redis(self):
		global redis_conn
		if not redis_conn:
			redis_config = current_app.config["REDIS"]
			host = redis_config["host"]
			port = redis_config["port"]
			db = redis_config["db"]
			password = redis_config["password"]
			redis_conn = StrictRedis(host=host, port=port, db=db, password=password)
		return redis_conn


class Base(RedisCfgMixin):
	def __init__(self, key, is_load, is_lock=False):
		self._key = key
		self._value = None
		self._has_load = False
		self._is_lock = is_lock
		if is_load:
			self.load()

	@property
	def key(self):
		return self._key

	@property
	def has_load(self):
		return self._has_load

	@property
	def value(self):
		return self._value

	def save_value(self, value):
		self._value = value
		self.save()

	def load(self):
		self._value = self.read()
		self._has_load = True

	def read(self):
		return None

	def format(self):
		return None

	def lock(self):
		key = ":".join(("redis_cache", self.key, "lock"))
		while True:
			ret = self.redis.setnx(key, "locking")
			if ret:
				self.redis.expire(key, 3600)
				return True
			time.sleep(10)

	def unlock(self):
		key = ":".join(("redis_cache", self.key, "lock"))
		self.redis.delete(key)

	def is_lock(self):
		key = ":".join(("redis_cache", self.key, "lock"))
		return self.redis.exists(key)

	def save(self):
		self._has_load = True

	def resave(self):
		self._value = self.format()
		self._has_load = True

		if self._is_lock:
			self.lock()

		self.save()
		if self._is_lock:
			self.unlock()

	def delete(self):
		return self.redis.delete(self.key)

	def exists(self):
		return self.redis.exists(self.key)

	def expire(self, seconds):
		return self.redis.expire(self.key, seconds)


class StringCache(Base):
	def __init__(self, key, is_load, is_lock=False):
		super(StringCache, self).__init__(key, is_load, is_lock)
		self._value = self._value or ""

	def read(self):
		return self.redis.get(self.key)

	def save_value(self, value, **kwargs):
		self._value = value
		self.save(**kwargs)

	def save(self, **kwargs):
		if self._value:
			self.redis.set(self.key, self._value, **kwargs)
		else:
			self.delete()
		super(StringCache, self).save()


class HashCache(Base):
	pass


class SetCache(Base):
	pass
