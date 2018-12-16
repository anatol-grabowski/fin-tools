import pandas as pd

fin_data = pd.DataFrame({'bid': [1.2, 1.4, 1.3], 'ask': [1.21, 1.43, 1.32]})
print(fin_data)

class Position:
    def __init__(self, size, tick):
        self.size = size
        self.opn = tick.bid if self.size > 0 else tick.ask
        self.clo = None
        self.profit = None

    def __repr__(self):
        return 'opn: %s, clo: %s, profit: %s' % (self.opn, self.clo, self.profit)

    def __str__(self):
        return self.__repr__()

    def close(self, tick):
        self.clo = tick.ask if self.size > 0 else tick.bid
        self.profit = self.clo - self.opn if self.size > 0 else self.opn - self.clo
