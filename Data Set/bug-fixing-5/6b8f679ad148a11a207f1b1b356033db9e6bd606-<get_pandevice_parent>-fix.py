def get_pandevice_parent(self, module):
    'Builds the pandevice object tree, returning the parent object.\n\n        If pandevice is not installed, then module.fail_json() will be\n        invoked.\n\n        Arguments:\n            * module(AnsibleModule): the ansible module.\n\n        Returns:\n            * The parent pandevice object based on the spec given to\n              get_connection().\n        '
    if (not HAS_PANDEVICE):
        module.fail_json(msg='Missing required library "pandevice".')
    if (self.min_pandevice_version is not None):
        pdv = tuple((int(x) for x in pandevice.__version__.split('.')))
        if (pdv < self.min_pandevice_version):
            module.fail_json(msg=_MIN_VERSION_ERROR.format('pandevice', pandevice.__version__, _vstr(self.min_pandevice_version)))
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
        self.device = PanDevice.create_from_device(d[host_arg], d['username'], d['password'], d['api_key'], d['port'])
    except PanDeviceError as e:
        module.fail_json(msg='Failed connection: {0}'.format(e))
    if (self.min_panos_version is not None):
        if (self.device._version_info < self.min_panos_version):
            module.fail_json(msg=_MIN_VERSION_ERROR.format('PAN-OS', _vstr(self.device._version_info), _vstr(self.min_panos_version)))
    parent = self.device
    not_found = '{0} "{1}" is not present.'
    pano_mia_param = 'Param "{0}" is required for Panorama but not specified.'
    ts_error = 'Specify either the template or the template stack{0}.'
    if hasattr(self.device, 'refresh_devices'):
        if (self.panorama_error is not None):
            module.fail_json(msg=self.panorama_error)
        tmpl_required = False
        added_template = False
        if (self.template_stack is not None):
            name = module.params[self.template_stack]
            if (name is not None):
                stacks = TemplateStack.refreshall(parent, name_only=True)
                for ts in stacks:
                    if (ts.name == name):
                        parent = ts
                        added_template = True
                        break
                else:
                    module.fail_json(msg=not_found.format('Template stack', name))
            elif (self.template is not None):
                tmpl_required = True
            else:
                module.fail_json(msg=pano_mia_param.format(self.template_stack))
        if (self.template is not None):
            name = module.params[self.template]
            if (name is not None):
                if added_template:
                    module.fail_json(msg=ts_error.format(', not both'))
                templates = Template.refreshall(parent, name_only=True)
                for t in templates:
                    if (t.name == name):
                        parent = t
                        break
                else:
                    module.fail_json(msg=not_found.format('Template', name))
            elif tmpl_required:
                module.fail_json(msg=ts_error.format(''))
            else:
                module.fail_json(msg=pano_mia_param.format(self.template))
        vsys_name = (self.vsys_importable or self.vsys)
        if (vsys_name is not None):
            name = module.params[vsys_name]
            if (name not in (None, 'shared')):
                vo = Vsys(name)
                parent.add(vo)
                parent = vo
        dg_name = (self.vsys_dg or self.device_group)
        if (dg_name is not None):
            name = module.params[dg_name]
            if (name not in (None, 'shared')):
                groups = DeviceGroup.refreshall(parent, name_only=True)
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
            elif (module.params[self.rulebase] == 'rulebase'):
                rb = Rulebase()
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
            self.device.vsys = module.params[vsys_name]
        if (self.rulebase is not None):
            rb = Rulebase()
            parent.add(rb)
            parent = rb
    return parent