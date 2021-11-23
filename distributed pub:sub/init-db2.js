db2 = db2.getSiblingDB("event2_db");
db2.event2_tb.drop();

db2.event2_tb.insert_many([
    {
        "event": 3,
        "data": "text",
        "subscription" : ["aaa","bbb"],
        "advertisement" : ["aaa"],
    },
    {
        "event": 4,
        "data": "text",
        "subscription" : ["aaa","bbb"],
        "advertisement" : ["bbb"],
    },
]);