import pytz
from datetime import datetime
capital_base = 1e7
start = datetime.strptime('Jan 1 2002', '%b %d %Y').replace(tzinfo=pytz.utc)
end = datetime.strptime('Jan 1 2004', '%b %d %Y').replace(tzinfo=pytz.utc)
from buyapple import initialize, handle_data


import zipline.data.loader as zipline_data_loader
def has_data_for_dates_stub(*args):
    print('stubbed has_data_for_dates(series_or_df, %s, %s) returned true' % args[1:])
    return True
zipline_data_loader.has_data_for_dates = has_data_for_dates_stub


import zipline
perf = zipline.run_algorithm(start=start, end=end, initialize=initialize, capital_base=capital_base)
print(len(perf))
