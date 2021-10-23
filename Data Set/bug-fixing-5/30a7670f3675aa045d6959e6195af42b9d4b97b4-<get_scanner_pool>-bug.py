def get_scanner_pool(self):
    '\n        Check to see if a scanner pool exist or not\n        :return: True if it exist, False if it does not\n        '
    scanner_pool_obj = netapp_utils.zapi.NaElement('vscan-scanner-pool-get-iter')
    scanner_pool_info = netapp_utils.zapi.NaElement('scan-scanner-pool-info')
    scanner_pool_info.add_new_child('scanner-pool', self.scanner_pool)
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(scanner_pool_info)
    scanner_pool_obj.add_child_elem(query)
    try:
        result = self.server.invoke_successfully(scanner_pool_obj, True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error searching for Vscan Scanner Pool %s: %s' % (self.scanner_pool, to_native(error))), exception=traceback.format_exc())
    if result.get_child_by_name('num-records'):
        if (result.get_child_by_name('attributes-list').get_child_by_name('vscan-scanner-pool-info').get_child_content('scanner-pool') == self.scanner_pool):
            return result.get_child_by_name('attributes-list').get_child_by_name('vscan-scanner-pool-info')
        return False
    return False