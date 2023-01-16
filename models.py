class Index:
    def __init__(self,name, full_name, price, date, time):
        self.name = name
        self.full_name = full_name
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

class PositionNamed:
    def __init__(self, position: Position, index_name):
        self.position = position
        self.index_name = index_name

    def __repr__(self) -> str:
        return "position: {}, index_name: {}".format(self.position, self.index_name)


class Portfolio:
    def __init__(self, funds, short_shares, long_shares, long, short, avg_buy_price_long, avg_buy_price_short,  pnl, number_of_trades, index_name):
        self.funds = funds
        self.short_shares = short_shares
        self.long_shares = long_shares
        self.long = long
        self.short = short
        self.avg_buy_price_long = avg_buy_price_long
        self.avg_buy_price_short = avg_buy_price_short
        self.pnl = pnl
        self.number_of_trades = number_of_trades
        self.index_name = index_name

    def __repr__(self) -> str:
        message = "Funds: {}\n" \
            "Short Shares: {}  \n"\
            "Long Shares: {} \n" \
            "Short: {}  \n"\
            "Long: {} \n" \
            "Avg Buy Price Short: {}  \n"\
            "Avg Buy Price Long: {} \n" \
            "PNL: {}\n" \
            "Total Trades: {}".format(round(self.funds, 3),
                                      round(self.short_shares, 3),
                                      round(self.long_shares, 3),
                                      round(self.short, 3),
                                      round(self.long, 3),
                                      round(self.avg_buy_price_short, 3),
                                      round(self.avg_buy_price_long, 3),
                                      self.pnl,
                                      self.number_of_trades)
        return message

class GlobalPortfolio:
    def __init__(self, funds, long, short, pnl, number_of_trades):
        self.funds = funds
        self.long = long
        self.short = short
        self.pnl = pnl
        self.number_of_trades = number_of_trades

    def __repr__(self) -> str:
        message = "Funds: {}\n" \
            "Short: {}  \n"\
            "Long: {} \n" \
            "PNL: {}\n" \
            "Total Trades: {}".format(round(self.funds, 3),
                                      round(self.short, 3),
                                      round(self.long, 3),
                                      self.pnl,
                                      self.number_of_trades)
        return message

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


class IndexConstituent:
    def __init__(self, name, weight_in_decimals):
        self.name = name
        self.weight_in_decimals = weight_in_decimals

class IndexConstituentSneaker:
    def __init__(self, name, weight_in_decimals, sku):
        self.name = name
        self.weight_in_decimals = weight_in_decimals
        self.sku = sku

class Tracker:
    def __init__(self, index_name, operator, target_price, sender, date, time):
        self.index_name = index_name
        self.operator = operator
        self.target_price = target_price
        self.sender = sender
        self.date = date
        self.time = time

class UserInputException(Exception):
    """ my custom exception class """
