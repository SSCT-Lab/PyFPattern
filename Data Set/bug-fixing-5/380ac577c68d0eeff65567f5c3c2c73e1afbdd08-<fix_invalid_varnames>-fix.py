def fix_invalid_varnames(self, data):
    "Change ':'' and '-' to '_' to ensure valid template variable names"
    for key in data:
        if ((':' in key) or ('-' in key)):
            newkey = key.replace(':', '_').replace('-', '_')
            data[newkey] = data.pop(key)