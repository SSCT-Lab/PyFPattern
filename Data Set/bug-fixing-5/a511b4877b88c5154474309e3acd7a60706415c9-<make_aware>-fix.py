def make_aware(value, timezone=None):
    '\n    Make a naive datetime.datetime in a given time zone aware.\n\n    :param value: datetime\n    :param timezone: timezone\n    :return: localized datetime in settings.TIMEZONE or timezone\n\n    '
    if (timezone is None):
        timezone = TIMEZONE
    if is_localized(value):
        raise ValueError(('make_aware expects a naive datetime, got %s' % value))
    if hasattr(value, 'fold'):
        value = value.replace(fold=1)
    if hasattr(timezone, 'localize'):
        return timezone.localize(value)
    elif hasattr(timezone, 'convert'):
        return timezone.convert(value)
    else:
        return value.replace(tzinfo=timezone)