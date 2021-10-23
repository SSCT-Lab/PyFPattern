def get_lun_mapping(self):
    'Find the matching lun mapping reference.\n\n        Returns: tuple(bool, int): contains volume match and volume mapping reference\n        '
    target_match = False
    reference = None
    if self.state:
        if (self.volume not in self.mapping_info['volume_by_name'].keys()):
            self.module.fail_json(msg=('Volume does not exist. Id [%s].' % self.ssid))
        if (self.target and (self.target not in self.mapping_info['target_by_name'].keys())):
            self.module.fail_json(msg=("Target does not exist. Id [%s'." % self.ssid))
    for lun_mapping in self.mapping_info['lun_mapping']:
        if (lun_mapping['volume_reference'] == self.mapping_info['volume_by_name'][self.volume]):
            reference = lun_mapping['lun_mapping_reference']
            if ((lun_mapping['map_reference'] in self.mapping_info['target_by_reference'].keys()) and (self.mapping_info['target_by_reference'][lun_mapping['map_reference']] == self.target)):
                target_match = True
    return (target_match, reference)