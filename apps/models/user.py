#! /usr/bin/env python
# coding:utf8

from . import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	__table_args__ = ({"mysql_engine": "InnoDB", "mysql_charset": "utf8"})
