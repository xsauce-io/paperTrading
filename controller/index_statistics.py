from pymongo import DESCENDING
from models import *
from .database import *

#Index
def add_index(index: Index):
     stats.insert_one(
            {"name": index.name , "full_name" : index.full_name ,"price": index.price, "date": index.date, "time": index.time})

def get_latest_index(index_name):
    # WARNING: This is hardcoded to get first element
    latest_index = stats.find({"name": index_name}).sort("_id", DESCENDING)[0]

    name = latest_index["name"]
    full_name = latest_index["full_name"]
    price = latest_index["price"]
    date = latest_index["date"]
    time = latest_index["time"]

    index = Index(name, full_name, price, date, time)
    return index

def get_all_latest_index(all_index_names):
    all_indexes = []
    for index_name in all_index_names:
        if (does_index_exist(index_name)):
            index = get_latest_index(index_name)
            all_indexes.append(index)
            print(index.name)

    return all_indexes


def does_index_exist(index_name) -> bool:
    index_stats = tuple(stats.find({"name": index_name}).clone())
    if (len(index_stats) > 0):
        return True
    else:
        return False
