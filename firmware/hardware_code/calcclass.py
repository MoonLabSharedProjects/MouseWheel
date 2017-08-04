from pymongo import MongoClient
import math

client = MongoClient()
db = client.wheel
session = db.dataset
diam = math.pi * 11
kmph = 0.036
speeds = []



def all_sessions():
    allsessions = session.distinct("session_id")#make index on session_id
    return allsessions

#calculates number of times/bouts mouse ran on the wheel
class Calc(object):
    def __init__(self, session_id):
        self.session_id = session_id
        xyz = session.find({"session_id": session_id, "interval_no": {'$gt': 0}})
        self.xyz = xyz
        intervals = xyz.distinct("interval_no")
        self.intervals = intervals
        weights = xyz.distinct("weight")
        self.weights = weights

    def allsessions(self):
        allsessions = session.distinct("session_id")
        return allsessions

    def interval_count(self):
        if len(self.intervals) and len(self.weights) != 0:
            numb = len(self.intervals)
            return numb
        else:
            return "N/A"

    def weightcalc(self):
        if sum(self.weights) != 0:
            weight = sum(self.weights)/len(self.weights)
            return round(weight, 2)
        else:
            return "N/A"

    def averagespeed(self):
        if len(self.weights) != 0:
            avrg = []
            for i in self.intervals:
                xyz1 = session.find({"session_id": self.session_id, "interval_no": i})
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
            average = (sum(speeds) / len(speeds)) * kmph
            return round(average, 3)
        else:
            return "N/A"


            #as above, but only returns the maximum speed in the "speeds" list
    def topspeed(self):
        if len(self.weights) != 0:
            avrg = []
            for i in self.intervals:
                xyz1 = session.find({"session_id": self.session_id, "interval_no": i})
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
            topspeed = max(speeds) * kmph
            return round(topspeed, 3)
        else:
            return "N/A"

#take the time between the first and last recorded timestamp
    def totaltime(self):
        if len(self.weights) != 0:
            times = []
            intervals = self.xyz.distinct("timestamp")
            for i in intervals:
                times.append(i)
            x = times[len(times) - 1] - times[0]
            return x
        else:
            return "N/A"


