

def is_update_required(self, original, proposed, optional_ignore=None):
    ' Compare original and proposed data to see if an update is needed '
    is_changed = False
    ignored_keys = ('id', 'organizationId')
    if (not optional_ignore):
        optional_ignore = ''
    for (k, v) in proposed.items():
        try:
            if ((k not in ignored_keys) and (k not in optional_ignore)):
                if (v != original[k]):
                    is_changed = True
        except KeyError:
            if (v != ''):
                is_changed = True
    return is_changed
