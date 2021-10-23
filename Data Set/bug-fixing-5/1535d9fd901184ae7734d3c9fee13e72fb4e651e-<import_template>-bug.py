def import_template(self, template_content, template_type='json'):
    update_rules = {
        'applications': {
            'createMissing': True,
            'deleteMissing': True,
        },
        'discoveryRules': {
            'createMissing': True,
            'updateExisting': True,
            'deleteMissing': True,
        },
        'graphs': {
            'createMissing': True,
            'updateExisting': True,
            'deleteMissing': True,
        },
        'httptests': {
            'createMissing': True,
            'updateExisting': True,
            'deleteMissing': True,
        },
        'items': {
            'createMissing': True,
            'updateExisting': True,
            'deleteMissing': True,
        },
        'templates': {
            'createMissing': True,
            'updateExisting': True,
        },
        'templateLinkage': {
            'createMissing': True,
        },
        'templateScreens': {
            'createMissing': True,
            'updateExisting': True,
            'deleteMissing': True,
        },
        'triggers': {
            'createMissing': True,
            'updateExisting': True,
            'deleteMissing': True,
        },
        'valueMaps': {
            'createMissing': True,
            'updateExisting': True,
        },
    }
    try:
        api_version = self._zapi.api_version()
        if (LooseVersion(api_version).version[:2] <= LooseVersion('3.2').version):
            update_rules['applications']['updateExisting'] = True
        import_data = {
            'format': template_type,
            'source': template_content,
            'rules': update_rules,
        }
        self._zapi.configuration.import_(import_data)
    except ZabbixAPIException as e:
        self._module.fail_json(msg='Unable to import template', details=to_native(e), exception=traceback.format_exc())