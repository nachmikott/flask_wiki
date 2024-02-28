class TimestampException(Exception):
    'the timestamp must be in YYYYMMDDHH format'
    pass

class UnexpectedDownstreamResponse(Exception):
    'recieved an unexpected response from a successful (Status code 200) downstream service.'
    pass
