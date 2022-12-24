def calculate_average_buy_price(amount_spent, purchased):
    avg_buy_price = amount_spent / purchased
    return avg_buy_price


def calculate_long_position(shares, avg_buy_price, index_price):
    long = (shares * avg_buy_price) + ((index_price - avg_buy_price) * shares)
    return long


def calculate_short_position(shares, avg_buy_price, index_price):
    short = (shares * avg_buy_price) + ((avg_buy_price - index_price) * shares)
    return short
