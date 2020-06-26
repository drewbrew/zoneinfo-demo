#!/usr/bin/env python3.7

import datetime
import sys

import pytz
from backports import zoneinfo


PYTZ_TIME_ZONE = pytz.timezone('America/Chicago')
ZONEINFO_TIME_ZONE = zoneinfo.ZoneInfo('America/Chicago')


def arithmetic_example(show_zoneinfo: bool = False):
    """Display the differences between zoneinfo and pytz in regards to DST boundaries"""

    if not show_zoneinfo:
        print("Next, we'll show how pytz handles date arithmetic around DST boundaries")
    else:
        print("Next, we'll show the difference as to how they handle date arithmetic around DST boundaries")

    # NOTE: Halloween 2020 is on a Saturday, so Sunday, November 1 is the end of DST
    # in the USA
    pytz_start = PYTZ_TIME_ZONE.localize(datetime.datetime(2020, 10, 31, 12))
    # pytz is quite literal: one day is 24 hours, so 24 hours after noon CDT is
    # 11 AM CDT
    next_day = PYTZ_TIME_ZONE.normalize(pytz_start + datetime.timedelta(days=1))
    print(f'One day after {pytz_start} using pytz is {next_day}')

    if not show_zoneinfo:
        return

    zoneinfo_start = datetime.datetime(2020, 10, 31, 12, tzinfo=ZONEINFO_TIME_ZONE)
    # whereas to humans, one day from noon is still noon, regardless of DST boundaries
    # so zoneinfo says one day later is noon CST
    next_day = zoneinfo_start + datetime.timedelta(days=1)
    print(f'One day after {zoneinfo_start} using zoneinfo is {next_day}')


def bad_pytz_usage_example(show_zoneinfo: bool = False):
    """Display how using pytz as a tzinfo arg is a bad idea"""

    # source:
    # https://blog.ganssle.io/articles/2018/03/pytz-fastest-footgun.html
    print("First, let's create noon CST on 2018-02-14 by passing the TZ as a tzinfo= argument to datetime.datetime()")

    dt = datetime.datetime(2018, 2, 14, 12, tzinfo=PYTZ_TIME_ZONE)
    # this prints an offset of -05:51 (because that's the oldest UTC offset in the TZ)
    print(f'Using a pytz zone as a tzinfo= parameter, we get {dt} (offset {dt.utcoffset()})')

    if not show_zoneinfo:
        return

    dt = datetime.datetime(2018, 2, 14, 12, tzinfo=ZONEINFO_TIME_ZONE)
    print(f'Using a zoneinfo zone as a tzinfo= parameter, we get {dt} (offset {dt.utcoffset()})')


if __name__ == '__main__':
    show_zoneinfo = len(sys.argv) > 1
    bad_pytz_usage_example(show_zoneinfo)
    print('')
    arithmetic_example(show_zoneinfo)
