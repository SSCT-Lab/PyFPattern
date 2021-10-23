def parse_model(self, data):
    prod_name = data.find('./data/system/node/mfg-info/product-name')
    if (prod_name is not None):
        return prod_name.text
    else:
        return ''