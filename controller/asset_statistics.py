from models import *
from typing import Type
from .database import *


#asset_statistic
def add_asset_statistic(asset: Type[Asset]):
    if type(asset) == Sneaker:
        asset_statistics.insert_one({"name": asset.name , "type": asset.type, "sku": asset.sku , "price": asset.price, "date": asset.date, "time": asset.time})
    else:
        asset_statistics.insert_one({"name": asset.name , "type": asset.type,  "price": asset.price, "date": asset.date, "time": asset.time})
