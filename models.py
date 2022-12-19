class Index :
    def __init__(self, price, date, time):
        self.price = price
        self.date = date
        self.time = time


class Position :
    def __init__(self, long_amount_spent, short_amount_spent, long_purchased, short_purchased, long_shares, short_shares, funds):
        self.long_amount_spent = long_amount_spent
        self.short_amount_spent = short_amount_spent
        self.long_purchased = long_purchased
        self.short_purchased = short_purchased
        self.long_shares = long_shares
        self.short_shares = short_shares
