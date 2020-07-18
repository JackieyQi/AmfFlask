#! /usr/bin/env python
# coding:utf8


REDIS = {
	"host": "localhost",
	"port": 6379,
	"db": 0,
	"password": "",
	"charset": "utf-8",
	"decode_responses": True
}

# MySQL
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/user?charset=utf8mb4'

SQLALCHEMY_TRACK_MODIFICATIONS = True
