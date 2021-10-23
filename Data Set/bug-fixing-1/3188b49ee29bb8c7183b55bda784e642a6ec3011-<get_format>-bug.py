

def get_format(format_type, lang=None, use_l10n=None):
    "\n    For a specific format type, returns the format for the current\n    language (locale), defaults to the format in the settings.\n    format_type is the name of the format, e.g. 'DATE_FORMAT'\n\n    If use_l10n is provided and is not None, that will force the value to\n    be localized (or not), overriding the value of settings.USE_L10N.\n    "
    format_type = force_str(format_type)
    if (use_l10n or ((use_l10n is None) and settings.USE_L10N)):
        if (lang is None):
            lang = get_language()
        cache_key = (format_type, lang)
        try:
            cached = _format_cache[cache_key]
            if (cached is not None):
                return cached
        except KeyError:
            for module in get_format_modules(lang):
                try:
                    val = getattr(module, format_type)
                    for iso_input in ISO_INPUT_FORMATS.get(format_type, ()):
                        if (iso_input not in val):
                            if isinstance(val, tuple):
                                val = list(val)
                            val.append(iso_input)
                    _format_cache[cache_key] = val
                    return val
                except AttributeError:
                    pass
            _format_cache[cache_key] = None
    if (format_type not in FORMAT_SETTINGS):
        return format_type
    return getattr(settings, format_type)
