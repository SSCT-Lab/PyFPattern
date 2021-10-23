

def _load_product_list(self, consumed=False):
    '\n            Loads list of all available or consumed pools for system in data structure\n\n            Args:\n                consumed(bool): if True list consumed  pools, else list available pools (default False)\n        '
    args = 'subscription-manager list'
    if consumed:
        args += ' --consumed'
    else:
        args += ' --available'
    (rc, stdout, stderr) = self.module.run_command(args, check_rc=True)
    products = []
    for line in stdout.split('\n'):
        line = line.strip()
        if (len(line) == 0):
            continue
        elif (':' in line):
            (key, value) = line.split(':', 1)
            key = key.strip().replace(' ', '')
            value = value.strip()
            if (key in ['ProductName', 'SubscriptionName']):
                products.append(RhsmPool(self.module, _name=value, key=value))
            elif products:
                products[(- 1)].__setattr__(key, value)
    return products
