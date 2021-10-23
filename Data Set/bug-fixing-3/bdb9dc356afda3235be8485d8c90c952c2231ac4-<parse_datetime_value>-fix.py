def parse_datetime_value(value):
    if (value[(- 1):] == 'Z'):
        value = value[:(- 1)]
    result = None
    try:
        result = datetime.strptime(value, DATE_FORMAT).replace(tzinfo=timezone.utc)
    except ValueError:
        pass
    else:
        return ((result, True), ((result + timedelta(days=1)), False))
    for format in [DATETIME_FORMAT, DATETIME_FORMAT_MICROSECONDS]:
        try:
            result = datetime.strptime(value, format).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
        else:
            break
    else:
        try:
            result = parse_unix_timestamp(value)
        except ValueError:
            pass
    if (result is None):
        raise InvalidQuery('{} is not a valid datetime query'.format(value))
    return (((result - timedelta(minutes=5)), True), ((result + timedelta(minutes=6)), False))