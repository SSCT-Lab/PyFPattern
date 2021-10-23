def compare_user(self, user, name, group_id, password, email):
    ' Compare user fields with new field values.\n\n        Returns:\n            false if user fields have some difference from new fields, true o/w.\n        '
    found_difference = ((name and (user['name'] != name)) or (password is not None) or (email and (user['email'] != email)) or (group_id and (user['current_group_id'] != group_id)))
    return (not found_difference)