def main():
    argument_spec = ucs_argument_spec
    argument_spec.update(org_name=dict(type='str', aliases=['name']), parent_org_path=dict(type='str', default='root'), description=dict(type='str', aliases=['descr']), state=dict(type='str', default='present', choices=['present', 'absent']), delegate_to=dict(type='str', default='localhost'))
    module = AnsibleModule(argument_spec, supports_check_mode=True, required_if=[['state', 'present', ['org_name']]])
    ucs = UCSModule(module)
    from ucsmsdk.mometa.org.OrgOrg import OrgOrg
    err = False
    changed = False
    requested_state = module.params['state']
    kwargs = dict()
    if (module.params['description'] is not None):
        kwargs['descr'] = module.params['description']
    try:
        parent_org_dn = ('org-' + module.params['parent_org_path'].replace('/', '/org-'))
        dn = ((parent_org_dn + '/org-') + module.params['org_name'])
        mo = ucs.login_handle.query_dn(dn)
        if mo:
            if (requested_state == 'present'):
                if (not mo.check_prop_match(**kwargs)):
                    changed = True
        elif (requested_state == 'present'):
            changed = True
        if (mo and (requested_state == 'absent')):
            changed = True
        if (changed and (not module.check_mode)):
            if (requested_state == 'absent'):
                ucs.login_handle.remove_mo(mo)
            else:
                kwargs['parent_mo_or_dn'] = parent_org_dn
                kwargs['name'] = module.params['org_name']
                if (module.params['description'] is not None):
                    kwargs['descr'] = module.params['description']
                mo = OrgOrg(**kwargs)
                ucs.login_handle.add_mo(mo, modify_present=True)
            ucs.login_handle.commit()
    except Exception as e:
        err = True
        ucs.result['msg'] = ('setup error: %s ' % str(e))
    ucs.result['changed'] = changed
    if err:
        module.fail_json(**ucs.result)
    module.exit_json(**ucs.result)