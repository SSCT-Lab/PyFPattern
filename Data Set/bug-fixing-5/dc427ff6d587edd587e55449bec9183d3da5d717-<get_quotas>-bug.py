def get_quotas(self):
    '\n        Get quota details\n        :return: name of volume if quota exists, None otherwise\n        '
    quota_get = netapp_utils.zapi.NaElement('quota-list-entries-iter')
    query = {
        'query': {
            'quota-entry': {
                'volume': self.parameters['volume'],
                'quota-target': self.parameters['quota_target'],
                'quota-type': self.parameters['type'],
            },
        },
    }
    quota_get.translate_struct(query)
    if self.parameters.get('policy'):
        quota_get['query']['quota-entry'].add_new_child('policy', self.parameters['policy'])
    try:
        result = self.server.invoke_successfully(quota_get, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error fetching quotas info: %s' % to_native(error)), exception=traceback.format_exc())
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        return_values = {
            'volume': result['attributes-list']['quota-entry']['volume'],
            'file_limit': result['attributes-list']['quota-entry']['file-limit'],
            'disk_limit': result['attributes-list']['quota-entry']['disk-limit'],
            'threshold': result['attributes-list']['quota-entry']['threshold'],
        }
        return return_values
    return None