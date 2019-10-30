import config
from pymongo import MongoClient
from flask import jsonify


def mongoDBHelper(dbName=config.MONGODB_NAME):
    global connection
    if not config.MONGODB_URI:
        connection = None
        return
    try:
        connection
    except NameError:
        connection = MongoClient(config.MONGODB_URI)
    db = connection[dbName]
    return db


def trueReturn(msg):
    return jsonify({
        'status': True,
        'data': msg,
        'message': ''
    })


def falseReturn(msg):
    return jsonify({
        'status': False,
        'data': '',
        'message': msg
    })
