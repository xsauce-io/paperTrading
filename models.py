class Index:
    def __init__(self, price, date, time):
        self.price = price
        self.date = date
        self.time = time


class Position:
    def __init__(self, long_amount_spent, short_amount_spent, long_purchased, short_purchased, long_shares, short_shares):
        self.long_amount_spent = long_amount_spent
        self.short_amount_spent = short_amount_spent
        self.long_purchased = long_purchased
        self.short_purchased = short_purchased
        self.long_shares = long_shares
        self.short_shares = short_shares

    def __repr__(self) -> str:
        return "long_amount_spent: {}, short_amount_spent: {}, long_purchased: {}, short_purchased: {}, long_shares: {}, short_shares: {}".format(self.long_amount_spent, self.short_amount_spent, self.long_purchased, self.short_purchased, self.long_shares, self.short_shares)


class Portfolio:
    def __init__(self, funds, short_shares, long_shares, long, short, avg_buy_price_long, avg_buy_price_short,  pnl, number_of_trades):
        self.funds = funds
        self.short_shares = short_shares
        self.long_shares = long_shares
        self.long = long
        self.short = short
        self.avg_buy_price_long = avg_buy_price_long
        self.avg_buy_price_short = avg_buy_price_short
        self.pnl = pnl
        self.number_of_trades = number_of_trades


class TradeDetails:
    def __init__(self, direction, amount, action, index_price, index_name, date, time):
        self.direction = direction
        self.amount = amount
        self.action = action
        self.index_price = index_price
        self.index_name = index_name
        self.date = date
        self.time = time

class Participant:
    def __init__(self, name, funds, number_of_trades):
        self.name = name
        self.funds = funds
        self.number_of_trades = number_of_trades

    def __repr__(self) -> str:
        return "name: {}, funds: {}, number_of_trades: {}".format(self.name, self.funds, self.number_of_trades)

class UserInputException(Exception):
    """ my custom exception class """
