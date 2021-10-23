def update_check(self, entity):

    def check_custom_properties():
        if self.param('custom_properties'):
            current = []
            if entity.custom_properties:
                current = [(cp.name, cp.regexp, str(cp.value)) for cp in entity.custom_properties]
            passed = [(cp.get('name'), cp.get('regexp'), str(cp.get('value'))) for cp in self.param('custom_properties') if cp]
            return (sorted(current) == sorted(passed))
        return True
    return (check_custom_properties() and equal(self.param('migratable'), getattr(entity, 'migratable', None)) and equal(self.param('pass_through'), entity.pass_through.mode.name) and equal(self.param('description'), entity.description) and equal(self.param('network_filter'), getattr(entity.network_filter, 'name', None)) and equal(self.param('qos'), entity.qos.name) and equal(self.param('port_mirroring'), getattr(entity, 'port_mirroring', None)))