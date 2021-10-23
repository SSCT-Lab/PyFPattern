def build_entity(self):
    return otypes.VnicProfile(name=self.param('name'), network=otypes.Network(id=self.__get_network_id()), description=(self.param('description') if self.param('description') else None), port_mirroring=self.param('port_mirroring'), pass_through=(otypes.VnicPassThrough(mode=otypes.VnicPassThroughMode(self.param('pass_through'))) if self.param('pass_through') else None), migratable=self.param('migratable'), custom_properties=([otypes.CustomProperty(name=cp.get('name'), regexp=cp.get('regexp'), value=str(cp.get('value'))) for cp in self.param('custom_properties') if cp] if (self.param('custom_properties') is not None) else None), qos=(otypes.Qos(id=self.__get_qos_id()) if self.param('qos') else None), network_filter=(otypes.NetworkFilter(id=self.__get_network_filter_id()) if self.param('network_filter') else None))