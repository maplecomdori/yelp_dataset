'''
Top 10 most common words in the reviews of "Chipotle Mexican Grill"
'''

from pymongo import MongoClient
import pprint

punctuation_list = ["`", ":", ",", "-", ".", "!", "(", ")", "{", "}", "[", "]", "<", ">", ".", "?", "'", '"', ";",
                    "/", "\\", "~", "!", "@", "#", "$", "%", "^", "&", "*", "+", "="]

# special cases
# i'm, you're, 's, you'd, great...except
# wasn't weren't don't aren't didn't won't shouldn't wouldn't
# 100%?

def delete_punctuations(string):
    if len(string) == 1:
        return string

    print(string)
    while len(string) > 0 and string[-1] in punctuation_list:
        string = string[:-1]
    while len(string) > 0 and string[0] in punctuation_list:
        string = string[1:]
    print(string)
    return string



client = MongoClient()
dblist = client.list_database_names()
db = client.yelp

# FIND CMG BUSINESS ID
cmg = db.business.find_one({"name": "Chipotle Mexican Grill"}, {"name": 1, "business_id": 1, "_id": 1, "city": 1})
# print(cmg)
cmg_id = cmg["business_id"]
# print(cmg_id)


query_review = {"business_id": cmg_id}
project_review = {"text": 1}
cmg_reviews = db.review.find(query_review, project_review)

# lst = list(cmg_reviews)
# line = lst[9]['text']

# print(line)
count_dict = {}

with open('all_words.txt', 'w')as f:
    # for w in line.split():
    #     f.write(w + "\n")
    #     clean = delete_punctuations(w.lower())
    #     f.write(clean + "\n")
    i = 0
    for r in cmg_reviews:
        i += 1
        words = r['text'].split()
        for w in words:
            w = w.lower()
            clean = delete_punctuations(w)
            if w not in count_dict:
                count_dict[clean] = 1
            else:
                count_dict[clean] += 1
            if w != clean:
                f.write(w + "\n" + clean + "\n")

        # print(words)
pp = pprint.PrettyPrinter(indent=4)
# print(i)

sorted_x = sorted(count_dict.items(), key=lambda kv: kv[1])
pp.pprint(sorted_x)