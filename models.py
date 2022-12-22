class Index :
    def __init__(self, price, date, time):
        self.price = price
        self.date = date
        self.time = time


class Position :
    def __init__(self, long_amount_spent, short_amount_spent, long_purchased, short_purchased, long_shares, short_shares):
        self.long_amount_spent = long_amount_spent
        self.short_amount_spent = short_amount_spent
        self.long_purchased = long_purchased
        self.short_purchased = short_purchased
        self.long_shares = long_shares
        self.short_shares = short_shares

class Portfolio :
    def __init__(self, funds, short_shares, long_shares, long, short, avg_buy_price_short, avg_buy_price_long, pnl, number_of_trades):
        self.funds = funds
        self.short_shares = short_shares
        self.long_shares = long_shares
        self.long = long
        self.short = short
        self.avg_buy_price_long = avg_buy_price_long
        self.avg_buy_price_short = avg_buy_price_short
        self.pnl = pnl
        self.number_of_trades = number_of_trades

class Trade :
    def __init__(self, direction, amount, action, index_price, index_name, date, time):
        self.direction = direction
        self.amount = amount
        self.action = action
        self.index_price = index_price
        self.index_name = index_name
        self.date = date
        self.time = time

class TradeDetails:
    def __init__(self, trades: list[Trade]):
        self.trades = trades

class Trades:
    def __init__(self, total, tradeDetails: list[Trade]):
        self.total = total
        self.tradeDetails = tradeDetails

class BuyIn:
    def __init__(self, purchased, amount_spent):
        self.purchased = purchased
        self.amount_spent = amount_spent

class Side:
    def __init__(self, share, buy_in: BuyIn):
       self.share = share

class position_n:
    def __init__(self, short: Side, long: Side ):
        self.short = short


class Participant:
     def __init__(self, username, funds, positions: list[Position], trades: Trades):
        self.username = username
        self.funds = funds
        self.positions = positions
        self.trades = trades
