class Position():
    def __init__(self, open_price, open_time):
        self.open_price = None
        self.close_price = None
        self.open_time = None
        self.close_time = None
        self.rprofit = None
        self.open(open_price, open_time)

    def __repr__(self):
        return '(o: %s, c: %s, pr: %s)' % (self.open_price, self.close_price, self.rprofit)

    def open(self, open_price, open_time):
        self.open_price = open_price
        self.open_time = open_time

    def close(self, close_price, close_time):
        rprofit = (close_price - self.open_price) / self.open_price
        self.close_price = close_price
        self.rprofit = rprofit