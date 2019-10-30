# -*- coding:utf-8 -*-
from flask import Blueprint, request
from ext import trueReturn

history = Blueprint('history', __name__)


# 状态收集接口
@history.route('/status', methods=['post'])
def post_status():
    from ext import mongoDBHelper
    data = request.json
    db = mongoDBHelper()
    db.history.insert(data)
    return trueReturn('success')


# 租户列表 distinct namespace
@history.route('/namespace', methods=['get'])
def get_namespace():
    from ext import mongoDBHelper
    db = mongoDBHelper()
    dataList = db.history.distinct("namespace")
    return trueReturn(dataList)


# 根据租户查该租户下的pod最新的一条
@history.route('/namespace/<namespace>', methods=['get'])
def get_pods_namespace(namespace):
    from ext import mongoDBHelper
    db = mongoDBHelper()
    dataList = db.history.aggregate([
        {'$match': {'namespace': namespace, 'containerName': {'$regex': 'moop'}}},
        {'$group': {'_id': '$containerName', 'lastid': {'$last': '$_id'}}},
        {"$lookup": {'from': 'history', 'localField': 'lastid', 'foreignField': '_id', 'as': 'detail'}}
    ])
    result = []
    for d in dataList:
        result.append({
            'name': d['detail'][0]['name'],
            'containerName': d['detail'][0]['containerName'],
            'namespace': d['detail'][0]['namespace'],
            'image': d['detail'][0]['image'],
            'status': d['detail'][0]['status'],
            'startAt': d['detail'][0]['startAt'],
            'collectTime': d['detail'][0]['collectTime'],
        })
    return trueReturn(result)


# pod列表，distinct container，需要去掉jupyter
@history.route('/pods', methods=['get'])
def get_pods():
    from ext import mongoDBHelper
    db = mongoDBHelper()
    dataList = db.history.distinct("containerName", {'containerName': {'$regex': 'moop'}})
    return trueReturn(dataList)


# 根据container，对比各租户的部署情况
@history.route('/pods/<pod>', methods=['get'])
def get_pod_list(pod):
    from ext import mongoDBHelper
    db = mongoDBHelper()
    dataList = db.history.aggregate([
        {'$match': {'containerName': pod}},
        {'$group': {'_id': '$namespace', 'lastid': {'$last': '$_id'}}},
        {"$lookup": {'from': 'history', 'localField': 'lastid', 'foreignField': '_id', 'as': 'detail'}}
    ])
    result = []
    for d in dataList:
        result.append({
            'name': d['detail'][0]['name'],
            'containerName': d['detail'][0]['containerName'],
            'namespace': d['detail'][0]['namespace'],
            'image': d['detail'][0]['image'],
            'status': d['detail'][0]['status'],
            'startAt': d['detail'][0]['startAt'],
            'collectTime': d['detail'][0]['collectTime'],
        })
    return trueReturn(result)
