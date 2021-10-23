def main():
    argument_spec = dict(name=dict(required=True, type='str'), description=dict(required=True, type='str'), parent_id=dict(required=False, type='int'), parent=dict(required=False, type='str'), state=dict(choices=['absent', 'present'], default='present'), quotas=dict(type='dict', default={
        
    }))
    argument_spec.update(manageiq_argument_spec())
    module = AnsibleModule(argument_spec=argument_spec)
    name = module.params['name']
    description = module.params['description']
    parent_id = module.params['parent_id']
    parent = module.params['parent']
    state = module.params['state']
    quotas = module.params['quotas']
    manageiq = ManageIQ(module)
    manageiq_tenant = ManageIQTenant(manageiq)
    (parent_tenant, tenant) = manageiq_tenant.tenant(name, parent_id, parent)
    if (state == 'absent'):
        if tenant:
            res_args = manageiq_tenant.delete_tenant(tenant)
        else:
            if parent_id:
                msg = ("tenant '%s' with parent_id %i does not exist in manageiq" % (name, parent_id))
            else:
                msg = ("tenant '%s' with parent '%s' does not exist in manageiq" % (name, parent))
            res_args = dict(changed=False, msg=msg)
    if (state == 'present'):
        if tenant:
            res_args = manageiq_tenant.edit_tenant(tenant, name, description)
        else:
            res_args = manageiq_tenant.create_tenant(name, description, parent_tenant)
            tenant = manageiq.client.get_entity('tenants', res_args['tenant_id'])
        if quotas:
            tenant_quotas_res = manageiq_tenant.update_tenant_quotas(tenant, quotas)
            if tenant_quotas_res['changed']:
                res_args['changed'] = True
                res_args['tenant_quotas_msg'] = tenant_quotas_res['msg']
        tenant.reload(expand='resources', attributes=['tenant_quotas'])
        res_args['tenant'] = manageiq_tenant.create_tenant_response(tenant, parent_tenant)
    module.exit_json(**res_args)