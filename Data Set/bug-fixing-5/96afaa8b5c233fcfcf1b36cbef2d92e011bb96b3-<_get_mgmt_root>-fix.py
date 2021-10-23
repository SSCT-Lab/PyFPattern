def _get_mgmt_root(self, type, **kwargs):
    if (type == 'bigip'):
        return BigIpMgmt(kwargs['server'], kwargs['user'], kwargs['password'], port=kwargs['server_port'], token='tmos')
    elif (type == 'iworkflow'):
        return iWorkflowMgmt(kwargs['server'], kwargs['user'], kwargs['password'], port=kwargs['server_port'], token='local')
    elif (type == 'bigiq'):
        return BigIqMgmt(kwargs['server'], kwargs['user'], kwargs['password'], port=kwargs['server_port'], auth_provider='local')