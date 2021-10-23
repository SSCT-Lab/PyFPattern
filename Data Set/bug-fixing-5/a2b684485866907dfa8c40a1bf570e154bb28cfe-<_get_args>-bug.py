def _get_args(self):
    args = {
        
    }
    args['name'] = self.module.params.get('name')
    args['displaytext'] = self.get_or_fallback('display_text', 'name')
    args['networkdomain'] = self.module.params.get('network_domain')
    args['networkofferingid'] = self.get_network_offering(key='id')
    return args