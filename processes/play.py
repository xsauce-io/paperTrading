import controller
from models import *


#public
def play(sender, id):

    if (sender == None):
        sender = str(id)
    if find_participant(sender):
        return("Nice try! No such thing as free")
    else:

        participant = create_participant(sender, id)
        if type(participant.name) == int:
            return("Welcome,\nThis is v0 of Daily Bread. Your account has been funded with $10,000")
        return("Welcome {},\nThis is v0 of Daily Bread. Your account has been funded with $10,000".format(participant.name))


def find_participant(sender):
    return controller.find_participant(sender)

def create_participant(sender,id):
    print(id)
    init_funds = 10000
    if (sender == None):
        sender = id
    participant = Participant(sender, init_funds, number_of_trades=0)
    controller.add_participant(participant.name, participant.funds)
    return participant