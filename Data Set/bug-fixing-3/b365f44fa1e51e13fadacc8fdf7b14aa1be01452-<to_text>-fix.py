def to_text(obj, encoding='utf-8', errors=None, nonstring='simplerepr'):
    "Make sure that a string is a text string\n\n    :arg obj: An object to make sure is a text string.  In most cases this\n        will be either a text string or a byte string.  However, with\n        ``nonstring='simplerepr'``, this can be used as a traceback-free\n        version of ``str(obj)``.\n    :kwarg encoding: The encoding to use to transform from a byte string to\n        a text string.  Defaults to using 'utf-8'.\n    :kwarg errors: The error handler to use if the byte string is not\n        decodable using the specified encoding.  Any valid `codecs error\n        handler <https://docs.python.org/2/library/codecs.html#codec-base-classes>`_\n        may be specified. On Python3 this defaults to 'surrogateescape'.  On\n        Python2, this defaults to 'replace'.\n    :kwarg nonstring: The strategy to use if a nonstring is specified in\n        ``obj``.  Default is 'simplerepr'.  Valid values are:\n\n        :simplerepr: The default.  This takes the ``str`` of the object and\n            then returns the text version of that string.\n        :empty: Return an empty text string\n        :passthru: Return the object passed in\n        :strict: Raise a :exc:`TypeError`\n\n    :returns: Typically this returns a text string.  If a nonstring object is\n        passed in this may be a different type depending on the strategy\n        specified by nonstring.  This will never return a byte string.\n    "
    if isinstance(obj, text_type):
        return obj
    if (errors in (None, 'surrogate_or_replace')):
        if HAS_SURROGATEESCAPE:
            errors = 'surrogateescape'
        else:
            errors = 'replace'
    elif (errors == 'surrogate_or_strict'):
        if HAS_SURROGATEESCAPE:
            errors = 'surrogateescape'
        else:
            errors = 'strict'
    if isinstance(obj, binary_type):
        return obj.decode(encoding, errors)
    if (nonstring == 'simplerepr'):
        try:
            value = str(obj)
        except UnicodeError:
            try:
                value = repr(obj)
            except UnicodeError:
                return ''
    elif (nonstring == 'passthru'):
        return obj
    elif (nonstring == 'empty'):
        return ''
    elif (nonstring == 'strict'):
        raise TypeError('obj must be a string type')
    else:
        raise TypeError(("Invalid value %s for to_text's nonstring parameter" % nonstring))
    return to_text(value, encoding, errors)