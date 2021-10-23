

def validate_fontweight(s):
    weights = ['ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black']
    if (s in weights):
        return s
    try:
        return int(s)
    except (ValueError, TypeError):
        raise ValueError(f'{s} is not a valid font weight.')
