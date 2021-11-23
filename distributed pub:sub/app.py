import sys
from flask import Flask, jsonify
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import service

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit_button'] == 'publisher':
            if request.form['pass'] == 'pppp':
                print('correct password!', file=sys.stderr)
                return redirect('/publishers')
            else:
                m = "Wrong Password"
                return render_template('index.html', msg=m)
                print('wrong password!', file=sys.stderr)
        elif request.form['submit_button'] == 'subscriber':
            if request.form['pass'] == 'ssss':
                print('correct password!', file=sys.stderr)
                return redirect('/subscribers')
            else:
                m = "Wrong Password"
                return render_template('index.html', msg=m)
                print('wrong password!', file=sys.stderr)
    return render_template('index.html')


@app.route('/publishers', methods=['GET', 'POST'])
def frompublishers():
    if request.method == 'POST':
        pid = request.form['publisherid']
        eid = int(request.form['dropdown'])
        if request.form['submit'] == 'advertise':
            m = service.advertise(pid, eid)
            return render_template('pub.html', msg=m)
        elif request.form['submit'] == 'deadvertise':
            m = service.deadvertise(pid, eid)
            return render_template('pub.html', msg=m)
        elif request.form['submit'] == 'publish':
            m = service.publish(pid, eid)
            return render_template('index.html', msg=m)
    return render_template('pub.html')


@app.route('/subscribers', methods=['GET', 'POST'])
def fromsubscribers():
    if request.method == 'POST':
        sid = request.form['subscriberid']
        eid = int(request.form['dropdown'])
        if request.form['submit'] == 'subscribe':
            m = service.subscribe(sid, eid)
            return render_template('sub.html', msg=m)
        elif request.form['submit'] == 'unsubscribe':
            m = service.unsubscribe(sid, eid)
            return render_template('sub.html', msg=m)
        if request.form['submit'] == 'updates':
            updates = service.notify(sid, eid)
            return render_template('sub.html', u=updates)
        elif request.form['submit'] == 'notifications':
            m = service.viewNotification(sid, eid)
            return render_template('sub.html', msg=m)
    return render_template('sub.html')


def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                         authSource="admin")
    db = client["event1_db"]
    return db


def get_events():
    db = ""
    try:
        db = get_db()
        db.event1_tb.insert_many([{
            "event": 1,
            "data": "jokes jokes",
            "subscription": ["aaa", "bbb"],
            "advertisement": ["aaa"],
        },
            {
                "event": 2,
                "data": "quotes quotes",
                "subscription": ["aaa", "bbb"],
                "advertisement": ["bbb"],
            }]
        )

        # db.event1_tb.update_many(
        #     {"event": 1},
        #     {"$set": {"data": "11111111"}})

        # db.event1_tb.delete_many(
        #                 {"event":{"$in":[1,2]}})

        _events = db.event1_tb.find()
        events = [{"event": event["event"], "data": event["data"], "subscription": event["subscription"],
                   "advertisement": event["advertisement"]} for event in _events]
        return jsonify({"events": events})
    except:
        pass
    finally:
        if type(db) == MongoClient:
            db.close()


def get_db2():
    client = MongoClient(host='test_mongodb2',
                         port=27018,
                         username='root',
                         password='pass',
                         authSource="admin")
    db2 = client["event2_db"]
    return db2


def get_event2():
    db2 = ""
    try:
        db2 = get_db2()
        db2.event2_tb.insert_many([{
            "event": 3,
            "data": "inspiration inspiration",
            "subscription": ["aaa", "bbb"],
            "advertisement": ["aaa"],
        },
            {
                "event": 4,
                "data": "something something",
                "subscription": ["aaa", "bbb"],
                "advertisement": ["bbb"],
            }])

        # db2.event2_tb.update_many(
        #     {"event": "topic4"},
        #     {"$set": {"data": "4444444"}})

        # db2.event2_tb.delete_many(
        #     {"event": {"$in": [3, 4]}})

        _events = db2.event2_tb.find()
        events = [{"event": event["event"], "data": event["data"], "subscription": event["subscription"],
                   "advertisement": event["advertisement"]} for event in _events]
        return jsonify({"events": events})
    except:
        pass
    finally:
        if type(db2) == MongoClient:
            db2.close()


get_events()
get_event2()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
