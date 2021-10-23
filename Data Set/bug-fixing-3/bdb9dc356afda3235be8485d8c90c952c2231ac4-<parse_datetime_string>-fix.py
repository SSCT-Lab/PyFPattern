def parse_datetime_string(value):
    if (value[(- 1):] == 'Z'):
        value = value[:(- 1)]
    for format in [DATETIME_FORMAT_MICROSECONDS, DATETIME_FORMAT, DATE_FORMAT]:
        try:
            return datetime.strptime(value, format).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    try:
        return parse_unix_timestamp(value)
    except ValueError:
        pass
    raise InvalidQuery('{} is not a valid datetime query'.format(value))