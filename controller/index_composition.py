from models import *
from .database import *

#Composition

def get_index_composition(index_name):
    index_composition = list(composition.find({"name": index_name})[0]['composition'])
    print(str(index_composition[0]))
    return index_composition

def does_index_composition_exist(index_name):
    index = list(composition.find({"name": index_name}).clone())
    print(index)
    if (len(index) > 0):
        return True
    else:
        return False
