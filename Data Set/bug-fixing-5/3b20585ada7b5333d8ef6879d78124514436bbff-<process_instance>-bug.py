def process_instance(self, instance, instance_type='virtual'):
    'Populate the inventory dictionary with any instance information'
    if (('status' in instance) and (instance['status']['name'] != 'Active')):
        return
    if (('powerState' in instance) and (instance['powerState']['name'] != 'Running')):
        return
    if (('hardwareStatusId' in instance) and (instance['hardwareStatusId'] != 5)):
        return
    if ('primaryIpAddress' not in instance):
        return
    dest = instance['primaryIpAddress']
    self.inventory['_meta']['hostvars'][dest] = instance
    if ('maxMemory' in instance):
        self.push(self.inventory, self.to_safe(('memory_' + str(instance['maxMemory']))), dest)
    elif ('memoryCapacity' in instance):
        self.push(self.inventory, self.to_safe(('memory_' + str(instance['memoryCapacity']))), dest)
    if ('maxCpu' in instance):
        self.push(self.inventory, self.to_safe(('cpu_' + str(instance['maxCpu']))), dest)
    elif ('processorPhysicalCoreAmount' in instance):
        self.push(self.inventory, self.to_safe(('cpu_' + str(instance['processorPhysicalCoreAmount']))), dest)
    self.push(self.inventory, self.to_safe(('datacenter_' + instance['datacenter']['name'])), dest)
    self.push(self.inventory, self.to_safe(instance['hostname']), dest)
    self.push(self.inventory, self.to_safe(instance['fullyQualifiedDomainName']), dest)
    self.push(self.inventory, self.to_safe(instance['domain']), dest)
    self.push(self.inventory, instance_type, dest)
    for tag in instance['tagReferences']:
        self.push(self.inventory, tag['tag']['name'], dest)