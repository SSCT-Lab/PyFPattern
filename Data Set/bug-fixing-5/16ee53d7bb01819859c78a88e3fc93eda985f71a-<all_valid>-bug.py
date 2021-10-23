def all_valid(formsets):
    'Return True if every formset in formsets is valid.'
    valid = True
    for formset in formsets:
        if (not formset.is_valid()):
            valid = False
    return valid