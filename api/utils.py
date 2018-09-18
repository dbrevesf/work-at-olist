"""
Module which contains several usefull methods to be used in this project
"""
from datetime import datetime


def standardize_date(date, pattern):
    """
    Method that standards a date object.

    Parameters:
        date (String/datetime): date object in string or datetime object
        pattern (string): the pattern that the time must match

    Return:
        date_datetime (Datetime.datetime): Date in a datetime standard
        format.
    """
    if isinstance(date, datetime):
        date = date.strftime(pattern)
    try:
        standard_date = datetime.strptime(date, pattern)
    except ValueError:
        error_msg = ('time date must match format %s' % (pattern))
        standard_date = {'input_error': error_msg}
    return standard_date
