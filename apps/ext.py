#! /usr/bin/env python
# coding:utf8

from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from celery import Celery


csrf = CSRFProtect()
db = SQLAlchemy()
celery = Celery()
