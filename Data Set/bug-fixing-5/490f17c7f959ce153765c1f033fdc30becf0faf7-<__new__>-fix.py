def __new__(cls, obj, *args, **kwargs):
    if isinstance(obj, AnsibleUnsafe):
        return obj
    if isinstance(obj, string_types):
        obj = AnsibleUnsafeText(to_text(obj, errors='surrogate_or_strict'))
    return obj