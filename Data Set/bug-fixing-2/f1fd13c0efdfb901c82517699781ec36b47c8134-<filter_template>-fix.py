

def filter_template(self, template_json):
    keep_keys = set(['graphs', 'templates', 'triggers', 'value_maps'])
    unwanted_keys = (set(template_json['zabbix_export']) - keep_keys)
    for unwanted_key in unwanted_keys:
        del template_json['zabbix_export'][unwanted_key]
    desc_not_supported = False
    if (LooseVersion(self._zapi.api_version()).version[:2] < LooseVersion('2.4').version):
        desc_not_supported = True
    for template in template_json['zabbix_export']['templates']:
        for key in list(template.keys()):
            if ((not template[key]) or ((key == 'description') and desc_not_supported)):
                template.pop(key)
    return template_json
