from datetime import datetime
import re


def get_current_date_time():
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime("%H:%M:%S")
    return date, time


def split_message(message):
    parsed_message = re.split("\s", message)
    return parsed_message


def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def rounder(num):
    rounded = round(num, 8)
    print('rounded')
    return rounded
