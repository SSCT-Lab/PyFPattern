def main():
    ' Module main '
    argument_spec = dict(state=dict(choices=['present', 'absent'], default='present'), authen_scheme_name=dict(type='str'), first_authen_mode=dict(default='local', choices=['invalid', 'local', 'hwtacacs', 'radius', 'none']), author_scheme_name=dict(type='str'), first_author_mode=dict(default='local', choices=['invalid', 'local', 'hwtacacs', 'if-authenticated', 'none']), acct_scheme_name=dict(type='str'), accounting_mode=dict(default='none', choices=['invalid', 'hwtacacs', 'radius', 'none']), domain_name=dict(type='str'), radius_server_group=dict(type='str'), hwtacas_template=dict(type='str'), local_user_group=dict(type='str'))
    argument_spec.update(ce_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    check_module_argument(module=module)
    changed = False
    proposed = dict()
    existing = dict()
    end_state = dict()
    updates = []
    state = module.params['state']
    authen_scheme_name = module.params['authen_scheme_name']
    first_authen_mode = module.params['first_authen_mode']
    author_scheme_name = module.params['author_scheme_name']
    first_author_mode = module.params['first_author_mode']
    acct_scheme_name = module.params['acct_scheme_name']
    accounting_mode = module.params['accounting_mode']
    domain_name = module.params['domain_name']
    radius_server_group = module.params['radius_server_group']
    hwtacas_template = module.params['hwtacas_template']
    local_user_group = module.params['local_user_group']
    ce_aaa_server = AaaServer()
    if (not ce_aaa_server):
        module.fail_json(msg='Error: init module failed.')
    proposed['state'] = state
    if authen_scheme_name:
        proposed['authen_scheme_name'] = authen_scheme_name
    if first_authen_mode:
        proposed['first_authen_mode'] = first_authen_mode
    if author_scheme_name:
        proposed['author_scheme_name'] = author_scheme_name
    if first_author_mode:
        proposed['first_author_mode'] = first_author_mode
    if acct_scheme_name:
        proposed['acct_scheme_name'] = acct_scheme_name
    if accounting_mode:
        proposed['accounting_mode'] = accounting_mode
    if domain_name:
        proposed['domain_name'] = domain_name
    if radius_server_group:
        proposed['radius_server_group'] = radius_server_group
    if hwtacas_template:
        proposed['hwtacas_template'] = hwtacas_template
    if local_user_group:
        proposed['local_user_group'] = local_user_group
    if authen_scheme_name:
        scheme_exist = ce_aaa_server.get_authentication_scheme(module=module)
        scheme_new = (authen_scheme_name.lower(), first_authen_mode.lower(), 'invalid')
        existing['authentication scheme'] = scheme_exist
        if (state == 'present'):
            if (len(scheme_exist) == 0):
                cmd = ce_aaa_server.create_authentication_scheme(module=module, authen_scheme_name=authen_scheme_name, first_authen_mode=first_authen_mode)
                updates.append(cmd)
                changed = True
            elif (scheme_new not in scheme_exist):
                cmd = ce_aaa_server.merge_authentication_scheme(module=module, authen_scheme_name=authen_scheme_name, first_authen_mode=first_authen_mode)
                updates.append(cmd)
                changed = True
            if domain_name:
                domain_exist = ce_aaa_server.get_authentication_domain(module=module)
                domain_new = (domain_name.lower(), authen_scheme_name.lower())
                if (len(domain_exist) == 0):
                    cmd = ce_aaa_server.create_authentication_domain(module=module, domain_name=domain_name, authen_scheme_name=authen_scheme_name)
                    updates.append(cmd)
                    changed = True
                elif (domain_new not in domain_exist):
                    cmd = ce_aaa_server.merge_authentication_domain(module=module, domain_name=domain_name, authen_scheme_name=authen_scheme_name)
                    updates.append(cmd)
                    changed = True
        elif (not domain_name):
            if (len(scheme_exist) == 0):
                pass
            elif (scheme_new not in scheme_exist):
                pass
            else:
                cmd = ce_aaa_server.delete_authentication_scheme(module=module, authen_scheme_name=authen_scheme_name, first_authen_mode=first_authen_mode)
                updates.append(cmd)
                changed = True
        else:
            domain_exist = ce_aaa_server.get_authentication_domain(module=module)
            domain_new = (domain_name.lower(), authen_scheme_name.lower())
            if (len(domain_exist) == 0):
                pass
            elif (domain_new not in domain_exist):
                pass
            else:
                cmd = ce_aaa_server.delete_authentication_domain(module=module, domain_name=domain_name, authen_scheme_name=authen_scheme_name)
                updates.append(cmd)
                changed = True
        scheme_end = ce_aaa_server.get_authentication_scheme(module=module)
        end_state['authentication scheme'] = scheme_end
    if author_scheme_name:
        scheme_exist = ce_aaa_server.get_authorization_scheme(module=module)
        scheme_new = (author_scheme_name.lower(), first_author_mode.lower(), 'invalid')
        existing['authorization scheme'] = scheme_exist
        if (state == 'present'):
            if (len(scheme_exist) == 0):
                cmd = ce_aaa_server.create_authorization_scheme(module=module, author_scheme_name=author_scheme_name, first_author_mode=first_author_mode)
                updates.append(cmd)
                changed = True
            elif (scheme_new not in scheme_exist):
                cmd = ce_aaa_server.merge_authorization_scheme(module=module, author_scheme_name=author_scheme_name, first_author_mode=first_author_mode)
                updates.append(cmd)
                changed = True
            if domain_name:
                domain_exist = ce_aaa_server.get_authorization_domain(module=module)
                domain_new = (domain_name.lower(), author_scheme_name.lower())
                if (len(domain_exist) == 0):
                    cmd = ce_aaa_server.create_authorization_domain(module=module, domain_name=domain_name, author_scheme_name=author_scheme_name)
                    updates.append(cmd)
                    changed = True
                elif (domain_new not in domain_exist):
                    cmd = ce_aaa_server.merge_authorization_domain(module=module, domain_name=domain_name, author_scheme_name=author_scheme_name)
                    updates.append(cmd)
                    changed = True
        elif (not domain_name):
            if (len(scheme_exist) == 0):
                pass
            elif (scheme_new not in scheme_exist):
                pass
            else:
                cmd = ce_aaa_server.delete_authorization_scheme(module=module, author_scheme_name=author_scheme_name, first_author_mode=first_author_mode)
                updates.append(cmd)
                changed = True
        else:
            domain_exist = ce_aaa_server.get_authorization_domain(module=module)
            domain_new = (domain_name.lower(), author_scheme_name.lower())
            if (len(domain_exist) == 0):
                pass
            elif (domain_new not in domain_exist):
                pass
            else:
                cmd = ce_aaa_server.delete_authorization_domain(module=module, domain_name=domain_name, author_scheme_name=author_scheme_name)
                updates.append(cmd)
                changed = True
        scheme_end = ce_aaa_server.get_authorization_scheme(module=module)
        end_state['authorization scheme'] = scheme_end
    if acct_scheme_name:
        scheme_exist = ce_aaa_server.get_accounting_scheme(module=module)
        scheme_new = (acct_scheme_name.lower(), accounting_mode.lower())
        existing['accounting scheme'] = scheme_exist
        if (state == 'present'):
            if (len(scheme_exist) == 0):
                cmd = ce_aaa_server.create_accounting_scheme(module=module, acct_scheme_name=acct_scheme_name, accounting_mode=accounting_mode)
                updates.append(cmd)
                changed = True
            elif (scheme_new not in scheme_exist):
                cmd = ce_aaa_server.merge_accounting_scheme(module=module, acct_scheme_name=acct_scheme_name, accounting_mode=accounting_mode)
                updates.append(cmd)
                changed = True
            if domain_name:
                domain_exist = ce_aaa_server.get_accounting_domain(module=module)
                domain_new = (domain_name.lower(), acct_scheme_name.lower())
                if (len(domain_exist) == 0):
                    cmd = ce_aaa_server.create_accounting_domain(module=module, domain_name=domain_name, acct_scheme_name=acct_scheme_name)
                    updates.append(cmd)
                    changed = True
                elif (domain_new not in domain_exist):
                    cmd = ce_aaa_server.merge_accounting_domain(module=module, domain_name=domain_name, acct_scheme_name=acct_scheme_name)
                    updates.append(cmd)
                    changed = True
        elif (not domain_name):
            if (len(scheme_exist) == 0):
                pass
            elif (scheme_new not in scheme_exist):
                pass
            else:
                cmd = ce_aaa_server.delete_accounting_scheme(module=module, acct_scheme_name=acct_scheme_name, accounting_mode=accounting_mode)
                updates.append(cmd)
                changed = True
        else:
            domain_exist = ce_aaa_server.get_accounting_domain(module=module)
            domain_new = (domain_name.lower(), acct_scheme_name.lower())
            if (len(domain_exist) == 0):
                pass
            elif (domain_new not in domain_exist):
                pass
            else:
                cmd = ce_aaa_server.delete_accounting_domain(module=module, domain_name=domain_name, acct_scheme_name=acct_scheme_name)
                updates.append(cmd)
                changed = True
        scheme_end = ce_aaa_server.get_accounting_scheme(module=module)
        end_state['accounting scheme'] = scheme_end
    if ((authen_scheme_name and (first_authen_mode.lower() == 'radius')) or (acct_scheme_name and (accounting_mode.lower() == 'radius'))):
        if (not radius_server_group):
            module.fail_json(msg='please input radius_server_group when use radius.')
        rds_template_exist = ce_aaa_server.get_radius_template(module=module)
        rds_template_new = radius_server_group
        rds_enable_exist = ce_aaa_server.get_radius_client(module=module)
        existing['radius template'] = rds_template_exist
        existing['radius enable'] = rds_enable_exist
        if (state == 'present'):
            if (len(rds_template_exist) == 0):
                cmd = ce_aaa_server.create_radius_template(module=module, radius_server_group=radius_server_group)
                updates.append(cmd)
                changed = True
            elif (rds_template_new not in rds_template_exist):
                cmd = ce_aaa_server.merge_radius_template(module=module, radius_server_group=radius_server_group)
                updates.append(cmd)
                changed = True
            rds_enable_new = 'true'
            if (rds_enable_new not in rds_enable_exist):
                cmd = ce_aaa_server.merge_radius_client(module=module, isEnable='true')
                updates.append(cmd)
                changed = True
        else:
            if (len(rds_template_exist) == 0):
                pass
            elif (rds_template_new not in rds_template_exist):
                pass
            else:
                cmd = ce_aaa_server.delete_radius_template(module=module, radius_server_group=radius_server_group)
                updates.append(cmd)
                changed = True
            rds_enable_new = 'false'
            if (rds_enable_new not in rds_enable_exist):
                cmd = ce_aaa_server.merge_radius_client(module=module, isEnable='false')
                updates.append(cmd)
                changed = True
            else:
                pass
        rds_template_end = ce_aaa_server.get_radius_template(module=module)
        end_state['radius template'] = rds_template_end
        rds_enable_end = ce_aaa_server.get_radius_client(module=module)
        end_state['radius enable'] = rds_enable_end
    tmp_scheme = author_scheme_name
    if ((authen_scheme_name and (first_authen_mode.lower() == 'hwtacacs')) or (tmp_scheme and (first_author_mode.lower() == 'hwtacacs')) or (acct_scheme_name and (accounting_mode.lower() == 'hwtacacs'))):
        if (not hwtacas_template):
            module.fail_json(msg='please input hwtacas_template when use hwtacas.')
        hwtacacs_exist = ce_aaa_server.get_hwtacacs_template(module=module)
        hwtacacs_new = hwtacas_template
        hwtacacs_enbale_exist = ce_aaa_server.get_hwtacacs_global_cfg(module=module)
        existing['hwtacacs template'] = hwtacacs_exist
        existing['hwtacacs enable'] = hwtacacs_enbale_exist
        if (state == 'present'):
            if (len(hwtacacs_exist) == 0):
                cmd = ce_aaa_server.create_hwtacacs_template(module=module, hwtacas_template=hwtacas_template)
                updates.append(cmd)
                changed = True
            elif (hwtacacs_new not in hwtacacs_exist):
                cmd = ce_aaa_server.merge_hwtacacs_template(module=module, hwtacas_template=hwtacas_template)
                updates.append(cmd)
                changed = True
            hwtacacs_enbale_new = 'true'
            if (hwtacacs_enbale_new not in hwtacacs_enbale_exist):
                cmd = ce_aaa_server.merge_hwtacacs_global_cfg(module=module, isEnable='true')
                updates.append(cmd)
                changed = True
        else:
            if (len(hwtacacs_exist) == 0):
                pass
            elif (hwtacacs_new not in hwtacacs_exist):
                pass
            else:
                cmd = ce_aaa_server.delete_hwtacacs_template(module=module, hwtacas_template=hwtacas_template)
                updates.append(cmd)
                changed = True
            hwtacacs_enbale_new = 'false'
            if (hwtacacs_enbale_new not in hwtacacs_enbale_exist):
                cmd = ce_aaa_server.merge_hwtacacs_global_cfg(module=module, isEnable='false')
                updates.append(cmd)
                changed = True
            else:
                pass
        hwtacacs_end = ce_aaa_server.get_hwtacacs_template(module=module)
        end_state['hwtacacs template'] = hwtacacs_end
        hwtacacs_enable_end = ce_aaa_server.get_hwtacacs_global_cfg(module=module)
        end_state['hwtacacs enable'] = hwtacacs_enable_end
    if local_user_group:
        user_group_exist = ce_aaa_server.get_local_user_group(module=module)
        user_group_new = local_user_group
        existing['local user group'] = user_group_exist
        if (state == 'present'):
            if (len(user_group_exist) == 0):
                cmd = ce_aaa_server.merge_local_user_group(module=module, local_user_group=local_user_group)
                updates.append(cmd)
                changed = True
            elif (user_group_new not in user_group_exist):
                cmd = ce_aaa_server.merge_local_user_group(module=module, local_user_group=local_user_group)
                updates.append(cmd)
                changed = True
        elif (len(user_group_exist) == 0):
            pass
        elif (user_group_new not in user_group_exist):
            pass
        else:
            cmd = ce_aaa_server.delete_local_user_group(module=module, local_user_group=local_user_group)
            updates.append(cmd)
            changed = True
        user_group_end = ce_aaa_server.get_local_user_group(module=module)
        end_state['local user group'] = user_group_end
    results = dict()
    results['proposed'] = proposed
    results['existing'] = existing
    results['changed'] = changed
    results['end_state'] = end_state
    results['updates'] = updates
    module.exit_json(**results)