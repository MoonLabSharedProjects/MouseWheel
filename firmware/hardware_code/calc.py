from pymongo import MongoClient
import math

client = MongoClient()
db = client.testwheel
session = db.dataset
diam = math.pi * 11
speeds = []

def weightcalc(session_id):
    xyz = session.find({"session_id": session_id, "interval_no": {'$gt': 0}})
    weights = xyz.distinct("weight")
    weight = sum(weights)/len(weights)
    return weight

def averagespeed(session_id):
    xyz = session.find({"session_id": session_id, "interval_no": {'$gt': 0}})
    intervals = xyz.distinct("interval_no")
    avrg = []
    for i in intervals:
        xyz1 = session.find({"session_id": session_id, "interval_no": i})
        ints = xyz1.distinct("timestamp")
        if len(ints) > 1:
            for i in ints:
                avrg.append(i)
            x = avrg[len(avrg) - 1] - avrg[0]
            time = x.total_seconds()
            distance = len(avrg) * diam
            speed = distance / time
            speeds.append(speed)
            del avrg[:]
    average = sum(speeds)/len(speeds)
    return average

def topspeed(session_id):
    xyz = session.find({"session_id": session_id, "interval_no": {'$gt': 0}})
    intervals = xyz.distinct("interval_no")
    avrg = []
    for i in intervals:
        xyz1 = session.find({"session_id": session_id, "interval_no": i})
        ints = xyz1.distinct("timestamp")
        if len(ints) > 1:
            for i in ints:
                avrg.append(i)
            x = avrg[len(avrg) - 1] - avrg[0]
            time = x.total_seconds()
            distance = len(avrg) * diam
            speed = distance / time
            speeds.append(speed)
            del avrg[:]
    topspeed = max(speeds)
    return topspeed