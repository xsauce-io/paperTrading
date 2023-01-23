from models import *
from .database import *


#Tracker
def add_index_tracker(index_name, operator, target_price, sender, date, time):
    trackers.insert_one(
            {"index_name": index_name, "operator": operator, "target_price": target_price, "username": sender, "date_created": date, "time_created": time, "deleted": False})

def get_all_trackers():
    result = trackers.find({"deleted": False})
    all_trackers:Tracker = []

    for tracker in result:
        index_name = tracker["index_name"]
        operator = tracker["operator"]
        target_price = tracker["target_price"]
        username = tracker["username"]
        date = tracker["date_created"]
        time = tracker["time_created"]

        tracker = Tracker(index_name, operator, target_price, username, date, time )

        all_trackers.append(tracker)
    return all_trackers

def delete_index_tracker(index_name, operator, target_price, sender):
    trackers.update_one({"username": sender, "operator": operator, "index_name": index_name, "target_price": target_price}, {"$set": {"deleted": True}})
