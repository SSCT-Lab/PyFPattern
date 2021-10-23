@staticmethod
def _parse_value(v):
    '\n        Attempt to transform the string value from an ini file into a basic python object\n        (int, dict, list, unicode string, etc).\n        '
    try:
        v = ast.literal_eval(v)
    except ValueError:
        pass
    except SyntaxError:
        pass
    return to_text(v, nonstring='passthru', errors='surrogate_or_strict')