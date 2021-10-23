def fix_invalid_varnames(self, data):
    "Change ':'' and '-' to '_' to ensure valid template variable names"
    for (key, value) in data.items():
        if ((':' in key) or ('-' in key)):
            newkey = key.replace(':', '_').replace('-', '_')
            del data[key]
            data[newkey] = value