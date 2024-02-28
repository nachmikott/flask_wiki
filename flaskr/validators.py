
from datetime import datetime
from flaskr.exceptions import TimestampException

def validate_timestamp(timestamp, no_day=False, no_hour=False):
    '''
    validates timestamp is the correct format

    Parameters:
    timestamp (string): the timestamp to determine is properly formatted to YYYYMM or YYYYMMDD.
    no_day (boolean): will check for YYYYMM
    no_hour: YYYYMMDD

    Returns:
    boolean: returns True if valid

    Raises:
    TimestampException --> parameter timestamp was not in format YYYYMMDD or YYYYMM
    '''
    day_format = '' if no_day else '%d'
    hour_format = '' if no_hour else '%H'
    date_format = f'%Y%m{day_format}{hour_format}'

    try:
        datetime.strptime(timestamp, date_format)
        return True
    except Exception as e:
        raise TimestampException(str(e))