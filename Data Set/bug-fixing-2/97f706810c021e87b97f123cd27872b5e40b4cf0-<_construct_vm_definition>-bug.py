

def _construct_vm_definition(self, kind, definition, template, params):
    self.client = self.get_api_client()
    disks = params.get('disks', [])
    memory = params.get('memory')
    memory_limit = params.get('memory_limit')
    cpu_cores = params.get('cpu_cores')
    cpu_model = params.get('cpu_model')
    cpu_features = params.get('cpu_features')
    labels = params.get('labels')
    datavolumes = params.get('datavolumes')
    interfaces = params.get('interfaces')
    bootloader = params.get('bootloader')
    cloud_init_nocloud = params.get('cloud_init_nocloud')
    machine_type = params.get('machine_type')
    headless = params.get('headless')
    smbios_uuid = params.get('smbios_uuid')
    hugepage_size = params.get('hugepage_size')
    tablets = params.get('tablets')
    cpu_shares = params.get('cpu_shares')
    cpu_limit = params.get('cpu_limit')
    template_spec = template['spec']
    if memory:
        template_spec['domain']['resources']['requests']['memory'] = memory
    if cpu_shares:
        template_spec['domain']['resources']['requests']['cpu'] = cpu_shares
    if cpu_limit:
        template_spec['domain']['resources']['limits']['cpu'] = cpu_limit
    if tablets:
        for tablet in tablets:
            tablet['type'] = 'tablet'
        template_spec['domain']['devices']['inputs'] = tablets
    if memory_limit:
        template_spec['domain']['resources']['limits']['memory'] = memory_limit
    if (hugepage_size is not None):
        template_spec['domain']['memory']['hugepages']['pageSize'] = hugepage_size
    if (cpu_features is not None):
        template_spec['domain']['cpu']['features'] = cpu_features
    if (cpu_cores is not None):
        template_spec['domain']['cpu']['cores'] = cpu_cores
    if cpu_model:
        template_spec['domain']['cpu']['model'] = cpu_model
    if labels:
        self.merge_dicts(template['metadata']['labels'], labels)
    if machine_type:
        template_spec['domain']['machine']['type'] = machine_type
    if bootloader:
        template_spec['domain']['firmware']['bootloader'] = {
            bootloader: {
                
            },
        }
    if smbios_uuid:
        template_spec['domain']['firmware']['uuid'] = smbios_uuid
    if (headless is not None):
        template_spec['domain']['devices']['autoattachGraphicsDevice'] = (not headless)
    self._define_disks(disks, template_spec)
    self._define_cloud_init(cloud_init_nocloud, template_spec)
    self._define_interfaces(interfaces, template_spec)
    self._define_datavolumes(datavolumes, definition['spec'])
    definition = dict(self.merge_dicts(self.resource_definitions[0], definition))
    resource = self.find_supported_resource(kind)
    return dict(self.merge_dicts(self.resource_definitions[0], definition))
