def build_entity(self):
    return otypes.VnicProfile(name=self.param('name'), network=otypes.Network(id=self._get_network_id()), description=(self.param('description') if (self.param('description') is not None) else None), pass_through=(otypes.VnicPassThrough(mode=otypes.VnicPassThroughMode(self.param('pass_through'))) if self.param('pass_through') else None), custom_properties=([otypes.CustomProperty(name=cp.get('name'), regexp=cp.get('regexp'), value=str(cp.get('value'))) for cp in self.param('custom_properties') if cp] if self.param('custom_properties') else None), migratable=self._get_migratable(), qos=self._get_qos(), port_mirroring=self._get_port_mirroring(), network_filter=self._get_network_filter())