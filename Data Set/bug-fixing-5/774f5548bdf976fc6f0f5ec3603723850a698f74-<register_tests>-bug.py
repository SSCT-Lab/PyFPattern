def register_tests(test_class, method_name, test_func, exclude=None):
    '\n    Dynamically create serializer tests to ensure that all registered\n    serializers are automatically tested.\n    '
    formats = [f for f in serializers.get_serializer_formats() if ((not isinstance(serializers.get_serializer(f), serializers.BadSerializer)) and (f != 'geojson') and ((exclude is None) or (f not in exclude)))]
    for format_ in formats:
        setattr(test_class, (method_name % format_), partialmethod(test_func, format_))