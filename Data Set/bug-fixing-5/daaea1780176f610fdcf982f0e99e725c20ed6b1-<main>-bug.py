def main():
    argument_spec = dict(description=dict(required=True, type='str'), state=dict(choices=['absent', 'present'], default='present'), role_id=dict(required=False, type='int'), role=dict(required=False, type='str'), tenant_id=dict(required=False, type='int'), tenant=dict(required=False, type='str'), managed_filters=dict(required=False, type='dict'), managed_filters_merge_mode=dict(required=False, choices=['merge', 'replace'], default='replace'), belongsto_filters=dict(required=False, type='list', elements='str'), belongsto_filters_merge_mode=dict(required=False, choices=['merge', 'replace'], default='replace'))
    argument_spec.update(manageiq_argument_spec())
    module = AnsibleModule(argument_spec=argument_spec)
    description = module.params['description']
    state = module.params['state']
    role_id = module.params['role_id']
    role_name = module.params['role']
    tenant_id = module.params['tenant_id']
    tenant_name = module.params['tenant']
    managed_filters = module.params['managed_filters']
    managed_filters_merge_mode = module.params['managed_filters_merge_mode']
    belongsto_filters = module.params['belongsto_filters']
    belongsto_filters_merge_mode = module.params['belongsto_filters_merge_mode']
    manageiq = ManageIQ(module)
    manageiq_group = ManageIQgroup(manageiq)
    group = manageiq_group.group(description)
    if (state == 'absent'):
        if group:
            res_args = manageiq_group.delete_group(group)
        else:
            res_args = dict(changed=False, msg=('group %s: does not exist in manageiq' % description))
    if (state == 'present'):
        tenant = manageiq_group.tenant(tenant_id, tenant_name)
        role = manageiq_group.role(role_id, role_name)
        norm_managed_filters = manageiq_group.normalize_user_managed_filters_to_sorted_dict(managed_filters, module)
        if group:
            res_args = manageiq_group.edit_group(group, description, role, tenant, norm_managed_filters, managed_filters_merge_mode, belongsto_filters, belongsto_filters_merge_mode)
        else:
            res_args = manageiq_group.create_group(description, role, tenant, norm_managed_filters, belongsto_filters)
            group = manageiq.client.get_entity('groups', res_args['group_id'])
        group.reload(expand='resources', attributes=['miq_user_role_name', 'tenant', 'entitlement'])
        res_args['group'] = manageiq_group.create_result_group(group)
    module.exit_json(**res_args)