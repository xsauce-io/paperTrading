import controller
from models import *



def asaux(sender, message):

    if controller.participants.does_participant_exist(sender) == False:
        raise UserInputException('You have no account yet. To start playing type /play')

    asaux_balance = controller.participants.get_participant_asaux_balance(sender)

    return asaux_balance
