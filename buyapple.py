from zipline.api import order, record, symbol


def initialize(context):
    context.asset = symbol('AAPL')


def handle_data(context, data):
    print('\n', context.datetime, data.current(context.asset, 'price'))
    order(context.asset, 10)
    record(AAPL=data.current(context.asset, 'price'))


# # Note: this function can be removed if running
# # this algorithm on quantopian.com
# def analyze(context=None, results=None):
#     import matplotlib.pyplot as plt
#     # Plot the portfolio and asset data.
#     ax1 = plt.subplot(211)
#     results.portfolio_value.plot(ax=ax1)
#     ax1.set_ylabel('Portfolio value (USD)')
#     ax2 = plt.subplot(212, sharex=ax1)
#     results.AAPL.plot(ax=ax2)
#     ax2.set_ylabel('AAPL price (USD)')

#     # Show the plot.
#     plt.gcf().set_size_inches(18, 8)
#     plt.show()
