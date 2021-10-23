def exec_module(self, **kwargs):
    for key in list(self.module_arg_spec.keys()):
        if hasattr(self, key):
            setattr(self, key, kwargs[key])
        elif (kwargs[key] is not None):
            self.body[key] = kwargs[key]
    self.inflate_parameters(self.module_arg_spec, self.body, 0)
    old_response = None
    response = None
    self.mgmt_client = self.get_mgmt_svc_client(GenericRestClient, base_url=self._cloud_environment.endpoints.resource_manager)
    resource_group = self.get_resource_group(self.resource_group)
    if ('location' not in self.body):
        self.body['location'] = resource_group.location
    self.url = ((((((((((('/subscriptions' + '/{{ subscription_id }}') + '/resourceGroups') + '/{{ resource_group }}') + '/providers') + '/Microsoft.Compute') + '/galleries') + '/{{ gallery_name }}') + '/images') + '/{{ image_name }}') + '/versions') + '/{{ version_name }}')
    self.url = self.url.replace('{{ subscription_id }}', self.subscription_id)
    self.url = self.url.replace('{{ resource_group }}', self.resource_group)
    self.url = self.url.replace('{{ gallery_name }}', self.gallery_name)
    self.url = self.url.replace('{{ image_name }}', self.gallery_image_name)
    self.url = self.url.replace('{{ version_name }}', self.name)
    old_response = self.get_resource()
    if (not old_response):
        self.log("GalleryImageVersion instance doesn't exist")
        if (self.state == 'absent'):
            self.log("Old instance didn't exist")
        else:
            self.to_do = Actions.Create
    else:
        self.log('GalleryImageVersion instance already exists')
        if (self.state == 'absent'):
            self.to_do = Actions.Delete
        else:
            modifiers = {
                
            }
            self.create_compare_modifiers(self.module_arg_spec, '', modifiers)
            self.results['modifiers'] = modifiers
            self.results['compare'] = []
            if (not self.default_compare(modifiers, self.body, old_response, '', self.results)):
                self.to_do = Actions.Update
    self.body.get('properties', {
        
    }).get('publishingProfile', {
        
    }).pop('snapshot', None)
    self.body.get('properties', {
        
    }).get('publishingProfile', {
        
    }).pop('managed_image', None)
    if ((self.to_do == Actions.Create) or (self.to_do == Actions.Update)):
        self.log('Need to Create / Update the GalleryImageVersion instance')
        if self.check_mode:
            self.results['changed'] = True
            return self.results
        response = self.create_update_resource()
        self.results['changed'] = True
        self.log('Creation / Update done')
    elif (self.to_do == Actions.Delete):
        self.log('GalleryImageVersion instance deleted')
        self.results['changed'] = True
        if self.check_mode:
            return self.results
        self.delete_resource()
    else:
        self.log('GalleryImageVersion instance unchanged')
        self.results['changed'] = False
        response = old_response
    if response:
        self.results['id'] = response['id']
        self.results['old_response'] = response
    return self.results