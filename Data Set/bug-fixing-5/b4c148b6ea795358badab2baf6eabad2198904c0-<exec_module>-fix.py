def exec_module(self, **kwargs):
    'Main module execution method'
    for key in list(self.module_arg_spec.keys()):
        if hasattr(self, key):
            setattr(self, key, kwargs[key])
        elif (kwargs[key] is not None):
            if (key == 'location'):
                self.parameters['location'] = kwargs[key]
            elif (key == 'collation'):
                self.parameters['collation'] = kwargs[key]
            elif (key == 'create_mode'):
                self.parameters['create_mode'] = _snake_to_camel(kwargs[key], True)
            elif (key == 'source_database_id'):
                self.parameters['source_database_id'] = kwargs[key]
            elif (key == 'source_database_deletion_date'):
                self.parameters['source_database_deletion_date'] = kwargs[key]
            elif (key == 'restore_point_in_time'):
                self.parameters['restore_point_in_time'] = kwargs[key]
            elif (key == 'recovery_services_recovery_point_resource_id'):
                self.parameters['recovery_services_recovery_point_resource_id'] = kwargs[key]
            elif (key == 'edition'):
                self.parameters['edition'] = _snake_to_camel(kwargs[key], True)
            elif (key == 'max_size_bytes'):
                self.parameters['max_size_bytes'] = kwargs[key]
            elif (key == 'elastic_pool_name'):
                self.parameters['elastic_pool_name'] = kwargs[key]
            elif (key == 'read_scale'):
                self.parameters['read_scale'] = ('Enabled' if kwargs[key] else 'Disabled')
            elif (key == 'sample_name'):
                ev = kwargs[key]
                if (ev == 'adventure_works_lt'):
                    ev = 'AdventureWorksLT'
                self.parameters['sample_name'] = ev
            elif (key == 'zone_redundant'):
                self.parameters['zone_redundant'] = (True if kwargs[key] else False)
    old_response = None
    response = None
    resource_group = self.get_resource_group(self.resource_group)
    if ('location' not in self.parameters):
        self.parameters['location'] = resource_group.location
    old_response = self.get_sqldatabase()
    if (not old_response):
        self.log("SQL Database instance doesn't exist")
        if (self.state == 'absent'):
            self.log("Old instance didn't exist")
        else:
            self.to_do = Actions.Create
    else:
        self.log('SQL Database instance already exists')
        if (self.state == 'absent'):
            self.to_do = Actions.Delete
        elif (self.state == 'present'):
            self.log('Need to check if SQL Database instance has to be deleted or may be updated')
            if (('location' in self.parameters) and (self.parameters['location'] != old_response['location'])):
                self.to_do = Actions.Update
            if (('read_scale' in self.parameters) and (self.parameters['read_scale'] != old_response['read_scale'])):
                self.to_do = Actions.Update
            if (('max_size_bytes' in self.parameters) and (self.parameters['max_size_bytes'] != old_response['max_size_bytes'])):
                self.to_do = Actions.Update
            if (('edition' in self.parameters) and (self.parameters['edition'] != old_response['edition'])):
                self.to_do = Actions.Update
    if ((self.to_do == Actions.Create) or (self.to_do == Actions.Update)):
        self.log('Need to Create / Update the SQL Database instance')
        if self.check_mode:
            self.results['changed'] = True
            return self.results
        response = self.create_update_sqldatabase()
        if (not old_response):
            self.results['changed'] = True
        else:
            self.results['changed'] = old_response.__ne__(response)
        self.log('Creation / Update done')
    elif (self.to_do == Actions.Delete):
        self.log('SQL Database instance deleted')
        self.results['changed'] = True
        if self.check_mode:
            return self.results
        self.delete_sqldatabase()
        while self.get_sqldatabase():
            time.sleep(20)
    else:
        self.log('SQL Database instance unchanged')
        self.results['changed'] = False
        response = old_response
    if response:
        self.results['id'] = response['id']
        self.results['database_id'] = response['database_id']
        self.results['status'] = response['status']
    return self.results