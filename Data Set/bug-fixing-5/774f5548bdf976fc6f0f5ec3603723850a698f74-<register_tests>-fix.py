def register_tests(test_class, method_name, test_func, exclude=()):
    '\n    Dynamically create serializer tests to ensure that all registered\n    serializers are automatically tested.\n    '
    for format_ in serializers.get_serializer_formats():
        if ((format_ == 'geojson') or (format_ in exclude)):
            continue
        decorated_func = skipIf(isinstance(serializers.get_serializer(format_), serializers.BadSerializer), ('The Python library for the %s serializer is not installed.' % format_))(test_func)
        setattr(test_class, (method_name % format_), partialmethod(decorated_func, format_))