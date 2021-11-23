from flask import Flask, jsonify
import pymongo
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import json
import random
import string
import datetime
import requests


# from eventService import get_text


# implementing routing
def get_db(eid):
    if eid == 1 or eid == 2:
        client = MongoClient(host='test_mongodb',
                             port=27017,
                             username='root',
                             password='pass',
                             authSource="admin")
        db = client["event1_db"]
    elif eid == 3 or eid == 4:
        client = MongoClient(host='test_mongodb2',
                             port=27018,
                             username='root',
                             password='pass',
                             authSource="admin")
        db = client["event2_db"]
    return db


# method to publish new data to selected events
def publish(pid, eid):
    db = ""
    db = get_db(eid)
    if eid == 1 or eid == 2:
        if eid == 1:
            headers = {'Accept': 'text/plain', }
            response = requests.get("https://icanhazdadjoke.com/", headers=headers)
            m = response.text
        elif eid == 2:
            headers = {'Accept': 'text/plain', }
            response = requests.get("https://api.adviceslip.com/advice", headers=headers)
            jj = json.loads(response.text)
            m = jj['slip']['advice']
        # x = datetime.datetime.now()
        # update = ("".join(random.choice(string.ascii_uppercase) for i in range(10))) + " from node 1 at topic : " + str(
        #     eid) + " @ " + str(
        #     x)
        update = m
        db.event1_tb.update_one(
            {"event": eid},
            {"$set": {"data": update}})
        _events = db.event1_tb.find({"event": eid})
    elif eid == 3 or eid == 4:
        if eid == 3:
            headers = {'Accept': 'text/plain', }
            response = requests.get("https://zenquotes.io/api/random", headers=headers)
            jjj = json.loads(response.text)
            m = jjj[0]['q']
        elif eid == 4:
            headers = {'Accept': 'text/plain', }
            response = requests.get("https://icanhazdadjoke.com/", headers=headers)
            m = response.text
        # x = datetime.datetime.now()
        # update = ("".join(random.choice(string.ascii_uppercase) for i in range(10))) + " from node 2 at topic : " + str(
        #     eid) + " @ " + str(
        #     x)
        update = m
        db.event2_tb.update_one(
            {"event": eid},
            {"$set": {"data": update}})
        _events = db.event2_tb.find({"event": eid})
    events = [{"event": event["event"], "data": event["data"], "advertisement": event["advertisement"]} for event in
              _events]
    if pid in events[0]["advertisement"]:
        if eid == 1:
            p = "Dad Jokes"
        elif eid == 2:
            p = "Random advice"
        elif eid == 3:
            p = "Inspirational quotes"
        elif eid == 4:
            p = "Alt Jokes"
        m = ('Exciting new ' + p + ' published by ' + pid)
    else:
        m = 'No ads to show :'
    return m


def advertise(pid, eid):
    db = ""
    db = get_db(eid)
    if eid == 1 or eid == 2:
        db.event1_tb.update({"event": eid}, {"$push": {"advertisement": pid}})
    elif eid == 3 or eid == 4:
        db.event2_tb.update({"event": eid}, {"$push": {"advertisement": pid}})
    m = pid + " will Advertise in " + str(eid)
    return m


def deadvertise(pid, eid):
    db = ""
    db = get_db(eid)
    if eid == 1 or eid == 2:
        db.event1_tb.update({"event": eid}, {"$pull": {"advertisement": pid}})
    elif eid == 3 or eid == 4:
        db.event2_tb.update({"event": eid}, {"$pull": {"advertisement": pid}})
    m = pid + " will not advertise in " + str(eid)
    return m


def subscribe(sid, eid):
    db = ""
    db = get_db(eid)
    if eid == 1 or eid == 2:
        db.event1_tb.update({"event": eid}, {"$push": {"subscription": sid}})
    elif eid == 3 or eid == 4:
        db.event2_tb.update({"event": eid}, {"$push": {"subscription": sid}})
    return "Subscribed"


def unsubscribe(sid, eid):
    db = ""
    db = get_db(eid)
    if eid == 1 or eid == 2:
        db.event1_tb.update({"event": eid}, {"$pull": {"subscription": sid}})
    elif eid == 3 or eid == 4:
        db.event2_tb.update({"event": eid}, {"$pull": {"subscription": sid}})
    return "Unsubscribed"


def notify(sid, eid):
    db = ""
    db = get_db(eid)
    if eid == 1 or eid == 2:
        _events = db.event1_tb.find({"event": eid})
    elif eid == 3 or eid == 4:
        _events = db.event2_tb.find({"event": eid})
    events = [{"event": event["event"], "data": event["data"], "subscription": event["subscription"]} for event in
              _events]
    if sid in events[0]["subscription"]:
        m = events[0]["data"]
    else:
        m = "Not subscribed"
    return m


def viewNotification(sid, eid):
    return "You have new notifications"
