

@register.filter(expects_localtime=True)
def naturalday(value, arg=None):
    '\n    For date values that are tomorrow, today or yesterday compared to\n    present day return representing string. Otherwise, return a string\n    formatted according to settings.DATE_FORMAT.\n    '
    try:
        tzinfo = getattr(value, 'tzinfo', None)
        value = date(value.year, value.month, value.day)
    except AttributeError:
        return value
    except ValueError:
        return value
    today = datetime.now(tzinfo).date()
    delta = (value - today)
    if (delta.days == 0):
        return _('today')
    elif (delta.days == 1):
        return _('tomorrow')
    elif (delta.days == (- 1)):
        return _('yesterday')
    return defaultfilters.date(value, arg)
