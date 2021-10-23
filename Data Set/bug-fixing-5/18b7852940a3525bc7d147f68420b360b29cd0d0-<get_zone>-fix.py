def get_zone(self, key=None):
    if self.zone:
        return self._get_by_key(key, self.zone)
    zone = self.module.params.get('zone')
    if (not zone):
        zone = os.environ.get('CLOUDSTACK_ZONE')
    zones = self.cs.listZones()
    if (not zones):
        self.module.fail_json(msg='No zones available. Please create a zone first')
    if (not zone):
        self.zone = zones['zone'][0]
        return self._get_by_key(key, self.zone)
    if zones:
        for z in zones['zone']:
            if (zone.lower() in [z['name'].lower(), z['id']]):
                self.zone = z
                return self._get_by_key(key, self.zone)
    self.module.fail_json(msg=("zone '%s' not found" % zone))