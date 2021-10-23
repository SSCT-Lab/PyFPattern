def serializer_factory(value):
    from django.db.migrations.writer import SettingsReference
    if isinstance(value, Promise):
        value = force_text(value)
    elif isinstance(value, LazyObject):
        value = value.__reduce__()[1][0]
    if isinstance(value, models.Field):
        return ModelFieldSerializer(value)
    if isinstance(value, models.manager.BaseManager):
        return ModelManagerSerializer(value)
    if isinstance(value, Operation):
        return OperationSerializer(value)
    if isinstance(value, type):
        return TypeSerializer(value)
    if hasattr(value, 'deconstruct'):
        return DeconstructableSerializer(value)
    if isinstance(value, frozenset):
        return FrozensetSerializer(value)
    if isinstance(value, list):
        return SequenceSerializer(value)
    if isinstance(value, set):
        return SetSerializer(value)
    if isinstance(value, tuple):
        return TupleSerializer(value)
    if isinstance(value, dict):
        return DictionarySerializer(value)
    if (enum and isinstance(value, enum.Enum)):
        return EnumSerializer(value)
    if isinstance(value, datetime.datetime):
        return DatetimeSerializer(value)
    if isinstance(value, datetime.date):
        return DateSerializer(value)
    if isinstance(value, datetime.time):
        return TimeSerializer(value)
    if isinstance(value, datetime.timedelta):
        return TimedeltaSerializer(value)
    if isinstance(value, SettingsReference):
        return SettingsReferenceSerializer(value)
    if isinstance(value, float):
        return FloatSerializer(value)
    if isinstance(value, (six.integer_types + (bool, type(None)))):
        return BaseSimpleSerializer(value)
    if isinstance(value, six.binary_type):
        return ByteTypeSerializer(value)
    if isinstance(value, six.text_type):
        return TextTypeSerializer(value)
    if isinstance(value, decimal.Decimal):
        return DecimalSerializer(value)
    if isinstance(value, functools.partial):
        return FunctoolsPartialSerializer(value)
    if isinstance(value, (types.FunctionType, types.BuiltinFunctionType)):
        return FunctionTypeSerializer(value)
    if isinstance(value, collections.Iterable):
        return IterableSerializer(value)
    if isinstance(value, (COMPILED_REGEX_TYPE, RegexObject)):
        return RegexSerializer(value)
    raise ValueError(('Cannot serialize: %r\nThere are some values Django cannot serialize into migration files.\nFor more, see https://docs.djangoproject.com/en/%s/topics/migrations/#migration-serializing' % (value, get_docs_version())))