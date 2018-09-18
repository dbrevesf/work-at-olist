"""
Module which contains several usefull methods to be used in this project
"""
from datetime import datetime


def standardize_date(date):
    """
    Method that standards a date object.

    Parameters:
        date (String/datetime): date object in string or datetime object

    Return:
        date_datetime (Datetime.datetime): Date in a datetime standard
        format.
    """
    pattern = '%Y-%m-%dT%H:%M:%SZ'
    if isinstance(date, datetime):
        date = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    try:
        standard_date = datetime.strptime(date, pattern)
    except ValueError:
        standard_date = {'input_error':
                         'Time date must match format YYYY-MM-DDTHH:MM:SSZ'}

    return standard_date
