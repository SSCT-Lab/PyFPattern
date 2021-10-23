def get_pandevice_parent(self, module):
    'Builds the pandevice object tree, returning the parent object.\n\n        If pandevice is not installed, then module.fail_json() will be\n        invoked.\n\n        Arguments:\n            * module(AnsibleModule): the ansible module.\n\n        Returns:\n            * The parent pandevice object based on the spec given to\n              get_connection().\n        '
    if (not HAS_PANDEVICE):
        module.fail_json(msg='Missing required library "pandevice".')
    (d, host_arg) = (None, None)
    if (module.params['provider'] and module.params['provider']['host']):
        d = module.params['provider']
        host_arg = 'host'
    elif (module.params['ip_address'] is not None):
        d = module.params
        host_arg = 'ip_address'
    else:
        module.fail_json(msg='New or classic provider params are required.')
    try:
        self.device = PanDevice.create_from_device(d[host_arg], d['username'], d['password'], d['api_key'])
    except PanDeviceError as e:
        module.fail_json(msg='Failed connection: {0}'.format(e))
    parent = self.device
    not_found = '{0} "{1}" is not present.'
    if hasattr(self.device, 'refresh_devices'):
        if (self.panorama_error is not None):
            module.fail_json(msg=self.panorama_error)
        if (self.template_stack is not None):
            name = module.params[self.template_stack]
            stacks = TemplateStack.refreshall(parent)
            for ts in stacks:
                if (ts.name == name):
                    parent = ts
                    break
            else:
                module.fail_json(msg=not_found.format('Template stack', name))
        if (self.template is not None):
            name = module.params[self.template]
            templates = Template.refreshall(parent)
            for t in templates:
                if (t.name == name):
                    parent = t
                    break
            else:
                module.fail_json(msg=not_found.format('Template', name))
        if (self.vsys_importable is not None):
            name = module.params[self.vsys_importable]
            if (name is not None):
                vo = Vsys(name)
                parent.add(vo)
                parent = vo
        dg_name = (self.vsys_dg or self.device_group)
        if (dg_name is not None):
            name = module.params[dg_name]
            if (name not in (None, 'shared')):
                groups = DeviceGroup.refreshall(parent)
                for dg in groups:
                    if (dg.name == name):
                        parent = dg
                        break
                else:
                    module.fail_json(msg=not_found.format('Device group', name))
        if (self.rulebase is not None):
            if (module.params[self.rulebase] in (None, 'pre-rulebase')):
                rb = PreRulebase()
                parent.add(rb)
                parent = rb
            elif (module.params[self.rulebase] == 'post-rulebase'):
                rb = PostRulebase()
                parent.add(rb)
                parent = rb
            else:
                module.fail_json(msg=not_found.format('Rulebase', module.params[self.rulebase]))
    else:
        if (self.firewall_error is not None):
            module.fail_json(msg=self.firewall_error)
        vsys_name = (self.vsys_dg or self.vsys or self.vsys_importable)
        if (vsys_name is not None):
            self.con.vsys = module.params[vsys_name]
        if (self.rulebase is not None):
            rb = Rulebase()
            parent.add(rb)
            parent = rb
    return parent