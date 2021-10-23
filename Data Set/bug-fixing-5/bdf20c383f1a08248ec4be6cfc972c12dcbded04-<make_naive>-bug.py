def make_naive(value, timezone=None):
    'Make an aware datetime.datetime naive in a given time zone.'
    if (timezone is None):
        timezone = get_current_timezone()
    if is_naive(value):
        raise ValueError('make_naive() cannot be applied to a naive datetime')
    value = value.astimezone(timezone)
    if hasattr(timezone, 'normalize'):
        value = timezone.normalize(value)
    return value.replace(tzinfo=None)