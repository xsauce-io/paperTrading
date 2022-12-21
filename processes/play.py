import controller
from models import *

def find_participant(sender):
    return controller.find_participant(sender)

def create_participant(sender):
    init_funds = 10000
    participant = Participant(sender, init_funds, position=None, trades=None)
    controller.add_participant(participant.name, participant.funds)
