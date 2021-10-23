def aos_login(module):
    mod_args = module.params
    aos = Session(server=mod_args['server'], port=mod_args['port'], user=mod_args['user'], passwd=mod_args['passwd'])
    try:
        aos.login()
    except aosExc.LoginServerUnreachableError:
        module.fail_json(msg=('AOS-server [%s] API not available/reachable, check server' % aos.server))
    except aosExc.LoginAuthError:
        module.fail_json(msg='AOS-server login credentials failed')
    module.exit_json(changed=False, ansible_facts=dict(aos_session=dict(url=aos.api.url, headers=aos.api.headers)), aos_session=dict(url=aos.api.url, headers=aos.api.headers))