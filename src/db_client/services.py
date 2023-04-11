import datetime
import json

from dateutil.relativedelta import relativedelta

from .deps import collection


async def aggregate_payments(dt_from: str, dt_upto: str,
                             group_type: str) -> str:

    dt_from = datetime.datetime.fromisoformat(dt_from)
    dt_upto = datetime.datetime.fromisoformat(dt_upto)

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
                "_id": {"$dateToString": {
                    "format": group_filter,
                    "date": "$dt"}
                },
                "sum_values": {"$sum": "$value"}
            }
        },
        {"$sort": {"_id": 1}}
    ]

    results = collection.aggregate(pipeline=pipeline)

    i = 0
    async for result in results:
        while result["_id"] != answer["labels"][i].strftime(group_filter):
            answer["dataset"].append(0)
            i += 1
        answer["dataset"].append(result["sum_values"])
        i += 1

    answer["dataset"].extend(
        [0 for x in range(len(answer["labels"])-len(answer["dataset"]))]
    )
    answer["labels"] = [x.isoformat() for x in answer["labels"]]
    
    return json.dumps(answer)
