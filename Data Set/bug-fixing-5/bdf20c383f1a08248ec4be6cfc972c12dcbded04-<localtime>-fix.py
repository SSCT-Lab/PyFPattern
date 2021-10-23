def localtime(value=None, timezone=None):
    '\n    Convert an aware datetime.datetime to local time.\n\n    Only aware datetimes are allowed. When value is omitted, it defaults to\n    now().\n\n    Local time is defined by the current time zone, unless another time zone\n    is specified.\n    '
    if (value is None):
        value = now()
    if (timezone is None):
        timezone = get_current_timezone()
    if is_naive(value):
        raise ValueError('localtime() cannot be applied to a naive datetime')
    return value.astimezone(timezone)