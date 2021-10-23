def get_aggr(self):
    '\n        Checks if aggregate exists.\n\n        :return:\n            True if aggregate found\n            False if aggregate is not found\n        :rtype: bool\n        '
    aggr_get_iter = netapp_utils.zapi.NaElement('aggr-get-iter')
    query_details = netapp_utils.zapi.NaElement.create_node_with_children('aggr-attributes', **{
        'aggregate-name': self.name,
    })
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(query_details)
    aggr_get_iter.add_child_elem(query)
    try:
        result = self.server.invoke_successfully(aggr_get_iter, enable_tunneling=False)
    except netapp_utils.zapi.NaApiError as error:
        if (to_native(error.code) == '13040'):
            return False
        else:
            self.module.fail_json(msg=to_native(error), exception=traceback.format_exc())
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        return True
    return False