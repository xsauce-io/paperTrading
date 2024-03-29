import controller
from models import *


#public

def play(sender):
    if (sender == None):
        return("You cannot play without a username. Please add a username to your telegram account")
    if does_participant_exist(sender):
        return("Nice try! No such thing as free")
    else:
        participant = create_participant(sender)
        if type(participant.name) == int:
            return("Welcome,\nThis is v0 of Daily Bread. Your account has been funded with $10,000")
        return("Welcome {},\nThis is v0 of Daily Bread. Your account has been funded with $10,000".format(participant.name))


def does_participant_exist(sender):
    return controller.participants.does_participant_exist(sender)


def create_participant(sender):
    print(id)
    init_funds = 10000
    participant = Participant(sender, init_funds, number_of_trades=0)
    controller.participants.add_participant(participant.name, participant.funds)
    return participant