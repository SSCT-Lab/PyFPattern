

def __new__(cls, obj, *args, **kwargs):
    if (isinstance(obj, string_types) and (not isinstance(obj, AnsibleUnsafeBytes))):
        obj = AnsibleUnsafeText(to_text(obj, errors='surrogate_or_strict'))
    return obj
