def get_nvme(self):
    '\n        Get current nvme details\n        :return: dict if nvme exists, None otherwise\n        '
    nvme_get = netapp_utils.zapi.NaElement('nvme-get-iter')
    query = {
        'query': {
            'nvme-target-service-info': {
                'vserver': self.parameters['vserver'],
            },
        },
    }
    nvme_get.translate_struct(query)
    try:
        result = self.server.invoke_successfully(nvme_get, enable_tunneling=False)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error fetching nvme info: %s' % to_native(error)), exception=traceback.format_exc())
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        attributes_list = result.get_child_by_name('attributes-list')
        nvme_info = attributes_list.get_child_by_name('nvme-target-service-info')
        return_value = {
            'status_admin': nvme_info.get_child_content('is-available'),
        }
        return return_value
    return None