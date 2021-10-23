def has_targets(available, required):
    '\n    Helper method to determine if mount tager requested already exists\n    '
    grouped = group_list_of_dict(available)
    for (value, field) in required:
        if ((field not in grouped) or (value not in grouped[field])):
            return False
    return True