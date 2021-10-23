

def exec_module(self, **kwargs):
    for key in self.module_arg_spec.keys():
        setattr(self, key, kwargs[key])
    self.get_resource_group(self.resource_group)
    zone = self.dns_client.zones.get(self.resource_group, self.zone_name)
    if (not zone):
        self.fail('The zone {0} does not exist in the resource group {1}'.format(self.zone_name, self.resource_group))
    try:
        self.log('Fetching Record Set {0}'.format(self.relative_name))
        record_set = self.dns_client.record_sets.get(self.resource_group, self.zone_name, self.relative_name, self.record_type)
        self.results['state'] = self.recordset_to_dict(record_set)
    except CloudError:
        record_set = None
    record_type_metadata = RECORDSET_VALUE_MAP.get(self.record_type)
    if (self.state == 'present'):
        self.input_sdk_records = self.create_sdk_records(self.records, self.record_type)
        if (not record_set):
            changed = True
        else:
            server_records = getattr(record_set, record_type_metadata.get('attrname'))
            (self.input_sdk_records, changed) = self.records_changed(self.input_sdk_records, server_records)
            changed |= (record_set.ttl != self.time_to_live)
        self.results['changed'] |= changed
    elif (self.state == 'absent'):
        if record_set:
            self.results['changed'] = True
    if self.check_mode:
        return self.results
    if self.results['changed']:
        if (self.state == 'present'):
            record_set_args = dict(ttl=self.time_to_live)
            record_set_args[record_type_metadata['attrname']] = (self.input_sdk_records if record_type_metadata['is_list'] else self.input_sdk_records[0])
            record_set = self.dns_models.RecordSet(**record_set_args)
            self.results['state'] = self.create_or_update(record_set)
        elif (self.state == 'absent'):
            self.delete_record_set()
    return self.results
