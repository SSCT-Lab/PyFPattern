def _get_args(self):
    args = {
        'name': self.module.params.get('name'),
        'displaytext': self.get_or_fallback('display_text', 'name'),
        'networkdomain': self.module.params.get('network_domain'),
        'networkofferingid': self.get_network_offering(key='id'),
    }
    return args