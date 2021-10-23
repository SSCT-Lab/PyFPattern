def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent', 'maintenance', 'upgraded', 'started', 'restarted', 'stopped', 'reinstalled'], default='present'), name=dict(required=True), comment=dict(default=None), cluster=dict(default=None), address=dict(default=None), password=dict(default=None, no_log=True), public_key=dict(default=False, type='bool', aliases=['ssh_public_key']), kdump_integration=dict(default=None, choices=['enabled', 'disabled']), spm_priority=dict(default=None, type='int'), override_iptables=dict(default=None, type='bool'), force=dict(default=False, type='bool'), timeout=dict(default=600, type='int'), override_display=dict(default=None), kernel_params=dict(default=None, type='list'), hosted_engine=dict(default=None, choices=['deploy', 'undeploy']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    check_sdk(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        hosts_service = connection.system_service().hosts_service()
        hosts_module = HostsModule(connection=connection, module=module, service=hosts_service)
        state = module.params['state']
        control_state(hosts_module)
        if (state == 'present'):
            hosts_module.create(deploy_hosted_engine=((module.params.get('hosted_engine') == 'deploy') if (module.params.get('hosted_engine') is not None) else None))
            ret = hosts_module.action(action='activate', action_condition=(lambda h: (h.status == hoststate.MAINTENANCE)), wait_condition=(lambda h: (h.status == hoststate.UP)), fail_condition=failed_state)
        elif (state == 'absent'):
            ret = hosts_module.remove()
        elif (state == 'maintenance'):
            hosts_module.action(action='deactivate', action_condition=(lambda h: (h.status != hoststate.MAINTENANCE)), wait_condition=(lambda h: (h.status == hoststate.MAINTENANCE)), fail_condition=failed_state)
            ret = hosts_module.create()
        elif (state == 'upgraded'):
            ret = hosts_module.action(action='upgrade', action_condition=(lambda h: h.update_available), wait_condition=(lambda h: (h.status == hoststate.UP)), fail_condition=failed_state)
        elif (state == 'started'):
            ret = hosts_module.action(action='fence', action_condition=(lambda h: (h.status == hoststate.DOWN)), wait_condition=(lambda h: (h.status in [hoststate.UP, hoststate.MAINTENANCE])), fail_condition=failed_state, fence_type='start')
        elif (state == 'stopped'):
            hosts_module.action(action='deactivate', action_condition=(lambda h: (h.status not in [hoststate.MAINTENANCE, hoststate.DOWN])), wait_condition=(lambda h: (h.status in [hoststate.MAINTENANCE, hoststate.DOWN])), fail_condition=failed_state)
            ret = hosts_module.action(action='fence', action_condition=(lambda h: (h.status != hoststate.DOWN)), wait_condition=(lambda h: ((h.status == hoststate.DOWN) if module.params['wait'] else True)), fail_condition=failed_state, fence_type='stop')
        elif (state == 'restarted'):
            ret = hosts_module.action(action='fence', wait_condition=(lambda h: (h.status == hoststate.UP)), fail_condition=failed_state, fence_type='restart')
        elif (state == 'reinstalled'):
            hosts_module.action(action='deactivate', action_condition=(lambda h: (h.status not in [hoststate.MAINTENANCE, hoststate.DOWN])), wait_condition=(lambda h: (h.status in [hoststate.MAINTENANCE, hoststate.DOWN])), fail_condition=failed_state)
            hosts_module.action(action='install', action_condition=(lambda h: (h.status == hoststate.MAINTENANCE)), post_action=hosts_module.post_reinstall, wait_condition=(lambda h: (h.status == hoststate.MAINTENANCE)), fail_condition=failed_state, host=(otypes.Host(override_iptables=module.params['override_iptables']) if module.params['override_iptables'] else None), root_password=module.params['password'], ssh=(otypes.Ssh(authentication_method=otypes.SshAuthenticationMethod.PUBLICKEY) if module.params['public_key'] else None), deploy_hosted_engine=((module.params.get('hosted_engine') == 'deploy') if (module.params.get('hosted_engine') is not None) else None), undeploy_hosted_engine=((module.params.get('hosted_engine') == 'undeploy') if (module.params.get('hosted_engine') is not None) else None))
            ret = hosts_module.action(action='activate', action_condition=(lambda h: (h.status == hoststate.MAINTENANCE)), wait_condition=(lambda h: (h.status == hoststate.UP)), fail_condition=failed_state)
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))