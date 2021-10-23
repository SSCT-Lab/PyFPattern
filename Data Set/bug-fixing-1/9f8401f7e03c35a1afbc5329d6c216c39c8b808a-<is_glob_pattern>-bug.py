

def is_glob_pattern(s):
    return (is_string(s) and (('*' in s) or ('?' is s)))
