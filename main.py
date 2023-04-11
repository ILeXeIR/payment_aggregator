import datetime
import json

from dateutil.relativedelta import relativedelta
from pymongo import MongoClient

from src.settings import settings


db_client = MongoClient(settings.mongodb_url)
db = db_client[settings.DB_NAME]
collection = db[settings.COLLECTION_NAME]

dt_from = datetime.datetime.fromisoformat("2022-09-01T00:00:00")
dt_upto = datetime.datetime.fromisoformat("2022-12-31T23:59:00")
group_type = "month"

answer = {"dataset": [], "labels": [dt_from]}

date_filter = {
    "$gte": dt_from,
    "$lte": dt_upto
}

if group_type == "month":
    group_filter = "%Y-%m"
    time_step = relativedelta(months=+1)
    next_date = dt_from + relativedelta(day=1, hour=0, minute=0, second=0,
                                        microsecond=0, months=+1)
elif group_type == "day":
    group_filter = "%Y-%m-%d"
    time_step = relativedelta(days=+1)
    next_date = dt_from + relativedelta(hour=0, minute=0, second=0,
                                        microsecond=0, days=+1)
elif group_type == "hour":
    group_filter = "%Y-%m-%d_%H"
    time_step = relativedelta(hours=+1)
    next_date = dt_from + relativedelta(minute=0, second=0, microsecond=0,
                                        hours=+1)

while next_date <= dt_upto:
    answer["labels"].append(next_date)
    next_date += time_step

pipeline = [
    {"$match": {"dt": date_filter}},
    {
        "$group": {
            "_id": {"$dateToString": {"format": group_filter, "date": "$dt"}},
            "sum_values": {"$sum": "$value"}
        }
    },
    {"$sort": {"_id": 1}}
]

results = list(collection.aggregate(pipeline=pipeline))

i = 0
for label in answer["labels"]:
    if i < len(results) and results[i]["_id"] == label.strftime(group_filter):
        answer["dataset"].append(results[i]["sum_values"])
        i += 1
    else:
        answer["dataset"].append(0)

answer["labels"] = [x.isoformat() for x in answer["labels"]]

print(json.dumps(answer))

