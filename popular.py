import re
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient()

    db = client.yelp

    query_dict = {"city": re.compile("toronto", re.IGNORECASE),
                  "state": "ON",
                  "review_count": {"$gt": 300},
                  "stars": {"$gte": 4.0}}
    fields_wanted = {"business_id": 1, "name": 1, "stars": 1, "review_count": 1}
    sort_dict = [("review_count", -1), ("stars", -1)]

    toronto_res = db.business.find(query_dict, fields_wanted).sort(sort_dict).limit(10)
    for x in toronto_res:
        print(x)

# possible popular measure
# #1: scale review_count out of 5 and calculate weighted average with stars and review_count
# I don't think making things complicated will end up with a better result