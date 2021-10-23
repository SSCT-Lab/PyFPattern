def constant_time_compare(val1, val2):
    'Return True if the two strings are equal, False otherwise.'
    return hmac.compare_digest(force_bytes(val1), force_bytes(val2))