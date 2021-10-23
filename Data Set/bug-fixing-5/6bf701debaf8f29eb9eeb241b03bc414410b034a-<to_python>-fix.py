@classmethod
def to_python(cls, data):
    values = []
    for (index, crumb) in enumerate(get_path(data, 'values', filter=True, default=())):
        try:
            values.append(cls.normalize_crumb(crumb))
        except Exception:
            pass
    return cls(values=values)