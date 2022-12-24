import controller
from models import *
import math
from helpers.utils import *

def add_index_statistics(name, full_name, price):
    index = create_index(name, full_name, price)
    controller.add_index(index)

def create_index(name, full_name, price):
    date,time = get_current_date_time()
    return Index(name, full_name, price, date, time)
