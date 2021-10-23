def exec_module(self, **kwargs):
    for key in self.module_arg_spec.keys():
        setattr(self, key, kwargs[key])
    resource_group = self.get_resource_group(self.resource_group)
    zone = self.dns_client.zones.get(self.resource_group, self.zone_name)
    if (not zone):
        self.fail('The zone {0} does not exist in the resource group {1}'.format(self.zone_name, self.resource_group))
    try:
        self.log('Fetching Record Set {0}'.format(self.relative_name))
        record_set = self.dns_client.record_sets.get(self.resource_group, self.zone_name, self.relative_name, self.record_type)
    except CloudError as ce:
        record_set = None
    if (self.state == 'present'):
        self.input_sdk_records = self.create_sdk_records(self.records)
        if (not record_set):
            changed = True
        else:
            server_records = getattr(record_set, self.record_type_metadata['attrname'])
            changed = self.records_changed(self.input_sdk_records, server_records)
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
            if (not self.record_type_metadata['is_list']):
                records_to_create_or_update = self.input_sdk_records[0]
            elif ((self.record_mode == 'append') and record_set):
                records_to_create_or_update = set(self.input_sdk_records).union(set(server_records))
            else:
                records_to_create_or_update = self.input_sdk_records
            record_set_args[self.record_type_metadata['attrname']] = records_to_create_or_update
            record_set = RecordSet(**record_set_args)
            rsout = self.dns_client.record_sets.create_or_update(self.resource_group, self.zone_name, self.relative_name, self.record_type, record_set)
        elif (self.state == 'absent'):
            self.delete_record_set()
    return self.results