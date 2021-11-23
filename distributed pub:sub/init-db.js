db = db.getSiblingDB("event1_db");
db.event1_tb.drop();

db.event1_tb.insert_many([
    {
        "event": 1,
        "data": "some joke",
        "subscription" : ["aaa","bbb"],
        "advertisement" : ["aaa"],

    },
    {
        "event": 2,
        "data": "Random advice",
        "subscription" : ["aaa","bbb"],
        "advertisement" : ["bbb"],
    },
]);