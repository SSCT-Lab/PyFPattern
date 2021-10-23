

def get_policy_group(self, policy_group_name=None):
    '\n        Return details of a policy group.\n        :param policy_group_name: policy group name\n        :return: policy group details.\n        :rtype: dict.\n        '
    if (policy_group_name is None):
        policy_group_name = self.parameters['name']
    policy_group_get_iter = netapp_utils.zapi.NaElement('qos-policy-group-get-iter')
    policy_group_info = netapp_utils.zapi.NaElement('qos-policy-group-info')
    policy_group_info.add_new_child('policy-group', policy_group_name)
    policy_group_info.add_new_child('vserver', self.parameters['vserver'])
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(policy_group_info)
    policy_group_get_iter.add_child_elem(query)
    result = self.server.invoke_successfully(policy_group_get_iter, True)
    policy_group_detail = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) == 1)):
        policy_info = result.get_child_by_name('attributes-list').get_child_by_name('qos-policy-group-info')
        policy_group_detail = {
            'name': policy_info.get_child_content('policy-group'),
            'vserver': policy_info.get_child_content('vserver'),
            'max_throughput': policy_info.get_child_content('max-throughput'),
            'min_throughput': policy_info.get_child_content('min-throughput'),
        }
    return policy_group_detail
