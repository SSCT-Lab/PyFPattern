def __init__(self):
    'Main path'
    self.inventory = self._empty_inventory()
    self.parse_options()
    if self.args.list:
        self.get_all_servers()
        print(self.json_format_dict(self.inventory, True))
    elif self.args.host:
        self.get_virtual_servers()
        print(self.json_format_dict(self.inventory['_meta']['hostvars'][self.args.host], True))