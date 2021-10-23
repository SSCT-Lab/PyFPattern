def import_template(self, template_json, template_name=None):
    parsed_template_json = self.load_json_template(template_json)
    if (template_name != parsed_template_json['zabbix_export']['templates'][0]['template']):
        self._module.fail_json(msg='JSON template name does not match presented name')
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
        if (LooseVersion(api_version) <= LooseVersion('3.2.x')):
            update_rules['applications']['updateExisting'] = True
        self._zapi.configuration.import_({
            'format': 'json',
            'source': template_json,
            'rules': update_rules,
        })
    except ZabbixAPIException as e:
        self._module.fail_json(msg='Unable to import JSON template', details=to_native(e), exception=traceback.format_exc())