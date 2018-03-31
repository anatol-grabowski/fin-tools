from datetime import time
from pytz import timezone
from pandas import date_range
from zipline.utils.calendars.trading_calendar import TradingCalendar, HolidayCalendar
from zipline.utils.calendars.calendar_utils import clear_calendars, register_calendar, get_calendar

from zipline.utils.memoize import lazyval

from pandas.tseries.offsets import CustomBusinessDay

class AnytimeCalendar(TradingCalendar):
    """
    Round the clock calendar: 7/7, 24/24
    """

    @property
    def name(self):
        return "ANYTIME"

    @property
    def tz(self):
        return timezone("Europe/London")

    @property
    def open_time(self):
        return time(0)

    @property
    def close_time(self):
        return time(23, 59)

    @property
    def regular_holidays(self):
        return []

    @property
    def special_opens(self):
        return []

    def sessions_in_range(self, start_session, last_session):
        return date_range(start_session, last_session)

    @lazyval
    def day(self):
        return CustomBusinessDay(holidays=self.adhoc_holidays,
        calendar=self.regular_holidays,weekmask="Mon Tue Wed Thu Fri Sat Sun")

#clear_calendars()
#register_calendar('ANYTIME', MyOwnCalendar)
#print('registered calendar', get_calendar('ANYTIME'))
