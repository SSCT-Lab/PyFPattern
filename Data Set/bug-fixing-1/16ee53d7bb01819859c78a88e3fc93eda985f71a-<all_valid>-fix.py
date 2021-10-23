

def all_valid(formsets):
    'Validate every formset and return True if all are valid.'
    valid = True
    for formset in formsets:
        valid &= formset.is_valid()
    return valid
