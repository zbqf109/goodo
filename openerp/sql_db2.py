#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""This file acts as a bridge between odoo's ORM model and database backend.
"""

import sqlalchemy
import sqlalchemy.engine.url
import openerp.tools.config

_pool = {}
sql_counter = 1


def db_connect(name):
    """Connect to the database named `name` and return a Connection object"""
    if name in _pool:
        return _pool[name].connection

    db_drive = openerp.tools.config.get("db_drive", "postgresql")
    db_user = openerp.tools.config.get("db_user")
    db_pass = openerp.tools.config.get("db_password")
    db_host = openerp.tools.config.get("db_host")
    db_port = openerp.tools.config.get("db_port")

    url = sqlalchemy.engine.url.URL(db_drive, db_user, db_pass, db_host, db_port, name)
    print 'connect to %s' % url
    # TODO shall we cache `engine`?
    engine = sqlalchemy.create_engine(url)
    # with engine.begin() as conn:
    #     return conn.connection
    connection = engine.connect()
    _pool[name] = connection
    return connection.connection


def close_all():
    for _, conn in _pool.items():
        conn.close()
    _pool.clear()


def close_db(db_name):
    conn = _pool.pop(db_name)
    if conn:
        conn.close()


def _build_dict(cr, row):
    return {d.name: row[i] for i, d in enumerate(cr.description)}

def dictfetchone(cr):
    row = cr.fetchone()
    return row and {d.name: row[i] for i, d in enumerate(cr.description)}


def dictfetchmany(cr, size):
    for row in cr.fetchmany(size):
        yield _build_dict(cr, row)


def dictfetchall(cr):
    for row in cr.fetchall():
        # yield {d.name: row[i] for i, d in enumerate(cr.description)}
        yield _build_dict(cr, row)

