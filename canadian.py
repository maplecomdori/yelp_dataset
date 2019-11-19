from pymongo import MongoClient
import pandas as pd
import pprint
import json

'''
How many Canadian residents(figure out who are Canadian residents by yourself) reviewed the business “Mon Ami Gabi” 
in last 1 year?
Canadian if:
    1. majority of the reviews are for restaurants in Canada (long term resident)
    2. majority of the reviews done in the past 6 months are for restaurants in Canada (6 months)?
'''

client = MongoClient()
dblist = client.list_database_names()
db = client.yelp
pp = pprint.PrettyPrinter(indent=4)

# FIND MAG BUSINESS ID
mon_ami_gabi = db.business.find_one({"name": "Mon Ami Gabi"}, {"name": 1, "business_id": 1, "_id": 1, "city": 1})
mag_business_id = mon_ami_gabi["business_id"]


# FIND CANADIAN BUSINESS
provinces = ["ON", "QC", "NS", "NB", "MB", "BC", "PE", "SK", "AB", "NL", "NT", "YT", "NU"]
cad_biz_query = {"state": {"$in": provinces}}
# biz_fields = {"business_id": 1, "name": 1, "city": 1, "state": 1}
biz_fields = {"business_id": 1}

canadian_business_ids = db.business.find(cad_biz_query, biz_fields)

df = pd.DataFrame(list(canadian_business_ids))
canadian_business_id_list = list(df.business_id)
set_canadian_business_id = set(canadian_business_id_list)
# print(set_canadian_business_id)


# DISTINCT USERS WHO HAVE REVIEWED MAG
review_query = {"business_id": mag_business_id, "date": {"$gt": "2018-01-01 00:00:00", "$lt": "2019-01-01 00:00:00"}}
project = {"user_id": 1, "review_id": 1, "_id": 0}
group = {"_id": "$user_id"}
pipeline = [
    {'$match': review_query},
    {'$project': project},
    {'$group': group},
]
cursor = db.review.aggregate(pipeline)
# print(len(list(cursor))) #951


# FIND ALL REVIEWS FOR EACH USER
mag_reviewers = []
i = 0
canadian_residents = []
for user in cursor:
    i += 1
    print(i)
    num_canadian_reviews = 0
    num_all_reviews = 0
    user_all_reviews = db.review.find({"user_id": user["_id"]}, {"review_id": 1, "user_id": 1, "business_id": 1, "_id": 0})
    for r in user_all_reviews:
        if r['business_id'] in set_canadian_business_id:
            num_canadian_reviews += 1
        num_all_reviews += 1

    if num_canadian_reviews / num_all_reviews >= 0.5:
        canadian_residents.append(user["_id"])


        dic = {user["_id"]: (num_all_reviews, num_canadian_reviews)}
        # print(dic)
        mag_reviewers.append(dic)

print(mag_reviewers)
with open('canadian.txt', 'w') as f:
    for r in mag_reviewers:
        f.write(json.dumps(r, indent=4, sort_keys=True))