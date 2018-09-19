"""
Module which contains several usefull methods to be used in this project
"""
from api import strings
import datetime


def standardize_date(date, pattern):
    """
    Standards a date object to make it easy to work with it.

    Parameters:
        date (String/datetime): date object in string or datetime object
        pattern (string): the pattern that the time must match

    Return:
        date_datetime (Datetime.datetime): Date in a datetime standard
        format.
    """
    if isinstance(date, datetime.datetime):
        date = date.strftime(pattern)
    try:
        standard_date = datetime.datetime.strptime(date, pattern)
    except ValueError:
        error_msg = (strings.TIME_PATTERN_ERROR % (pattern))
        standard_date = {strings.INPUT_ERROR_KEY: error_msg}
    return standard_date


def get_period_between_time(start, end):
    """
    Calculates the period between two datetime.time values.

    Parameters:
        start (datetime.time): starting time
        end (datetime.time): ending time

    Return:
        period (int): period between start and end in minutes

    """
    period_hour = 0
    period_minute = 0
    if start.hour > end.hour:
        period_hour = 24 - start.hour + end.hour
    else:
        period_hour = end.hour - start.hour
    if start.minute > end.minute:
        period_minute = 60 - start.minute + end.minute
    else:
        period_minute = end.minute - start.minute
    period = 60 * period_hour + period_minute
    return period


def get_last_month_period():
    """
    Returns the month before the current month combined with the current year.

    Return:
        period (string): YYYY-MM, where YYYY is current year and MM is the last
        month.
    """
    current_month = datetime.datetime.now().month
    last_month = current_month - 1
    current_year = datetime.datetime.now().year
    period = ('%s-%s' % (current_year, last_month))
    return period
