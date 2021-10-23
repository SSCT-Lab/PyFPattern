def control_state(host_module):
    host = host_module.search_entity()
    if (host is None):
        return
    state = host_module._module.params['state']
    host_service = host_module._service.service(host.id)
    if failed_state(host):
        if ((hoststate.INSTALL_FAILED == host.status) and (state != 'reinstalled')):
            raise Exception(("Not possible to manage host '%s' in state '%s'." % (host.name, host.status)))
    elif (host.status in [hoststate.REBOOT, hoststate.CONNECTING, hoststate.INITIALIZING, hoststate.INSTALLING, hoststate.INSTALLING_OS]):
        wait(service=host_service, condition=(lambda host: (host.status == hoststate.UP)), fail_condition=failed_state)
    elif (host.status == hoststate.PREPARING_FOR_MAINTENANCE):
        wait(service=host_service, condition=(lambda host: (host.status == hoststate.MAINTENANCE)), fail_condition=failed_state)