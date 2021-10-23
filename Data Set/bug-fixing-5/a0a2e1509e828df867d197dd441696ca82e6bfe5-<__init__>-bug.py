def __init__(self, load=True):
    self.inventory = self._empty_inventory()
    if load:
        self.parse_cli_args()
        self.read_settings()
        cache_valid = self.is_cache_valid()
        if (self.args.refresh_cache or (not cache_valid)):
            self.do_api_calls_update_cache()
        else:
            self.inventory = self.get_inventory_from_cache()