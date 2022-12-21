def calculate_long_position(shares, avg_buy_price, index_price):
    long = (shares * avg_buy_price) + ((index_price - avg_buy_price) * shares)
    return long
