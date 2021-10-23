def get_qtree(self, name=None):
    '\n        Checks if the qtree exists.\n\n        :return:\n            True if qtree found\n            False if qtree is not found\n        :rtype: bool\n        '
    if (name is None):
        name = self.name
    qtree_list_iter = netapp_utils.zapi.NaElement('qtree-list-iter')
    query_details = netapp_utils.zapi.NaElement.create_node_with_children('qtree-info', **{
        'vserver': self.vserver,
        'volume': self.flexvol_name,
        'qtree': name,
    })
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(query_details)
    qtree_list_iter.add_child_elem(query)
    result = self.server.invoke_successfully(qtree_list_iter, enable_tunneling=True)
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        return True
    else:
        return False