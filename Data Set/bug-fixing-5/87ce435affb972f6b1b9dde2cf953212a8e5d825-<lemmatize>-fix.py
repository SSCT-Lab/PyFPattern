def lemmatize(string, index, exceptions, rules):
    string = string.lower()
    forms = []
    if (string in index):
        forms.append(string)
        return forms
    forms.extend(exceptions.get(string, []))
    oov_forms = []
    if (not forms):
        for (old, new) in rules:
            if string.endswith(old):
                form = (string[:(len(string) - len(old))] + new)
                if (not form):
                    pass
                elif ((form in index) or (not form.isalpha())):
                    forms.append(form)
                else:
                    oov_forms.append(form)
    if (not forms):
        forms.extend(oov_forms)
    if ((not forms) and (string in LOOKUP.keys())):
        forms.append(LOOKUP[string])
    if (not forms):
        forms.append(string)
    return list(set(forms))