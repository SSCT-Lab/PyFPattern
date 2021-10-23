def parse_datetime_value(value):
    if (value[(- 1)] == 'Z'):
        value = value[:(- 1)]
    if (len(value) in (8, 10)):
        value = datetime.strptime(value, DATE_FORMAT).replace(tzinfo=timezone.utc)
        return ((value, True), ((value + timedelta(days=1)), False))
    if (value[4] == '-'):
        try:
            value = datetime.strptime(value, DATETIME_FORMAT).replace(tzinfo=timezone.utc)
        except ValueError:
            value = datetime.strptime(value, DATETIME_FORMAT_MICROSECONDS).replace(tzinfo=timezone.utc)
    else:
        value = parse_unix_timestamp(value)
    return (((value - timedelta(minutes=5)), True), ((value + timedelta(minutes=6)), False))