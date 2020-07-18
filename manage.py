#! /usr/bin/env python
# coding:utf8

import click
from flask.cli import FlaskGroup

from apps import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
	pass


@cli.command("create-user")
@click.argument("name")
def create_user(name):
	print(name)
	return


if __name__ == "__main__":
	cli()
