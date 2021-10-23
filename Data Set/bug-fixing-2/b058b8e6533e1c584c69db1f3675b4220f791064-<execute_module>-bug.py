

def execute_module(self):
    "\n        Performs basic CRUD operations on the model object. Ends by calling\n        AnsibleModule.fail_json(), if an error is encountered, otherwise\n        AnsibleModule.exit_json() with a dict containing:\n          changed: boolean\n          api_version: the API version\n          <kind>: a dict representing the object's state\n        :return: None\n        "
    if self.params.get('debug'):
        self.helper.enable_debug(reset_logfile=False)
        self.helper.log_argspec()
    resource_definition = self.params.get('resource_definition')
    if self.params.get('src'):
        resource_definition = self.load_resource_definition(self.params['src'])
    if resource_definition:
        resource_params = self.resource_to_parameters(resource_definition)
        self.params.update(resource_params)
    state = self.params.get('state', None)
    force = self.params.get('force', False)
    dry_run = self.params.pop('dry_run', False)
    name = self.params.get('name')
    namespace = self.params.get('namespace', None)
    existing = None
    return_attributes = dict(changed=False, api_version=self.api_version, request=self.helper.request_body_from_params(self.params))
    return_attributes[self.helper.base_model_name_snake] = {
        
    }
    if dry_run:
        self.exit_json(**return_attributes)
    try:
        auth_options = {
            
        }
        for (key, value) in self.helper.argspec.items():
            if (value.get('auth_option') and (self.params.get(key) is not None)):
                auth_options[key] = self.params[key]
        self.helper.set_client_config(**auth_options)
    except KubernetesException as e:
        self.fail_json(msg='Error loading config', error=str(e))
    if (state is None):
        if self.helper.base_model_name_snake.endswith('list'):
            k8s_obj = self._read(name, namespace)
            return_attributes[self.kind] = k8s_obj.to_dict()
            self.exit_json(**return_attributes)
        elif self.helper.has_method('create'):
            k8s_obj = self._create(namespace)
            return_attributes[self.kind] = k8s_obj.to_dict()
            return_attributes['changed'] = True
            self.exit_json(**return_attributes)
        else:
            self.fail_json(msg='Missing state parameter. Expected one of: present, absent')
    try:
        existing = self.helper.get_object(name, namespace)
    except KubernetesException as exc:
        self.fail_json(msg='Failed to retrieve requested object: {}'.format(exc.message), error=exc.value.get('status'))
    if (state == 'absent'):
        if (not existing):
            self.exit_json(**return_attributes)
        else:
            if (not self.check_mode):
                try:
                    self.helper.delete_object(name, namespace)
                except KubernetesException as exc:
                    self.fail_json(msg='Failed to delete object: {}'.format(exc.message), error=exc.value.get('status'))
            return_attributes['changed'] = True
            self.exit_json(**return_attributes)
    else:
        if (not existing):
            k8s_obj = self._create(namespace)
            return_attributes[self.kind] = k8s_obj.to_dict()
            return_attributes['changed'] = True
            self.exit_json(**return_attributes)
        if (existing and force):
            k8s_obj = None
            request_body = self.helper.request_body_from_params(self.params)
            if (not self.check_mode):
                try:
                    k8s_obj = self.helper.replace_object(name, namespace, body=request_body)
                except KubernetesException as exc:
                    self.fail_json(msg='Failed to replace object: {}'.format(exc.message), error=exc.value.get('status'))
            return_attributes[self.kind] = k8s_obj.to_dict()
            return_attributes['changed'] = True
            self.exit_json(**return_attributes)
        k8s_obj = copy.deepcopy(existing)
        try:
            self.helper.object_from_params(self.params, obj=k8s_obj)
        except KubernetesException as exc:
            self.fail_json(msg='Failed to patch object: {}'.format(exc.message))
        (match, diff) = self.helper.objects_match(existing, k8s_obj)
        if match:
            return_attributes[self.kind] = existing.to_dict()
            self.exit_json(**return_attributes)
        else:
            self.helper.log('Existing:')
            self.helper.log(existing.to_str(), indent=4)
            self.helper.log('\nDifferences:')
            self.helper.log(json.dumps(diff, indent=4))
        if (not self.check_mode):
            try:
                k8s_obj = self.helper.patch_object(name, namespace, k8s_obj)
            except KubernetesException as exc:
                self.fail_json(msg='Failed to patch object: {}'.format(exc.message))
        return_attributes[self.kind] = k8s_obj.to_dict()
        return_attributes['changed'] = True
        self.exit_json(**return_attributes)
