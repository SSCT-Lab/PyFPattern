def get_formats():
    '\n    Returns all formats strings required for i18n to work\n    '
    FORMAT_SETTINGS = ('DATE_FORMAT', 'DATETIME_FORMAT', 'TIME_FORMAT', 'YEAR_MONTH_FORMAT', 'MONTH_DAY_FORMAT', 'SHORT_DATE_FORMAT', 'SHORT_DATETIME_FORMAT', 'FIRST_DAY_OF_WEEK', 'DECIMAL_SEPARATOR', 'THOUSAND_SEPARATOR', 'NUMBER_GROUPING', 'DATE_INPUT_FORMATS', 'TIME_INPUT_FORMATS', 'DATETIME_INPUT_FORMATS')
    result = {
        
    }
    for module in ([settings] + get_format_modules(reverse=True)):
        for attr in FORMAT_SETTINGS:
            result[attr] = get_format(attr)
    formats = {
        
    }
    for (k, v) in result.items():
        if isinstance(v, (six.string_types, int)):
            formats[k] = smart_text(v)
        elif isinstance(v, (tuple, list)):
            formats[k] = [smart_text(value) for value in v]
    return formats