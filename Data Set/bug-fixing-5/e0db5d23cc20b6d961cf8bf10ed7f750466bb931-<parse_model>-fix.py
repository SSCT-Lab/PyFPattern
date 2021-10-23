def parse_model(self, data):
    prod_name = data.find('./data/system-sw-state/sw-version/sw-platform')
    if (prod_name is not None):
        return prod_name.text
    else:
        return ''