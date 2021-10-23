def connect_to_api(module, disconnect_atexit=True):
    hostname = module.params['hostname']
    username = module.params['username']
    password = module.params['password']
    port = module.params.get('port', 443)
    validate_certs = module.params['validate_certs']
    if (not hostname):
        module.fail_json(msg="Hostname parameter is missing. Please specify this parameter in task or export environment variable like 'export VMWARE_HOST=ESXI_HOSTNAME'")
    if (not username):
        module.fail_json(msg="Username parameter is missing. Please specify this parameter in task or export environment variable like 'export VMWARE_USER=ESXI_USERNAME'")
    if (not password):
        module.fail_json(msg="Password parameter is missing. Please specify this parameter in task or export environment variable like 'export VMWARE_PASSWORD=ESXI_PASSWORD'")
    if (validate_certs and (not hasattr(ssl, 'SSLContext'))):
        module.fail_json(msg='pyVim does not support changing verification mode with python < 2.7.9. Either update python or use validate_certs=false.')
    ssl_context = None
    if ((not validate_certs) and hasattr(ssl, 'SSLContext')):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ssl_context.verify_mode = ssl.CERT_NONE
    service_instance = None
    try:
        service_instance = connect.SmartConnect(host=hostname, user=username, pwd=password, sslContext=ssl_context, port=port)
    except vim.fault.InvalidLogin as invalid_login:
        module.fail_json(msg=('Unable to log on to vCenter or ESXi API at %s:%s as %s: %s' % (hostname, port, username, invalid_login.msg)))
    except vim.fault.NoPermission as no_permission:
        module.fail_json(msg=('User %s does not have required permission to log on to vCenter or ESXi API at %s:%s : %s' % (username, hostname, port, no_permission.msg)))
    except (requests.ConnectionError, ssl.SSLError) as generic_req_exc:
        module.fail_json(msg=('Unable to connect to vCenter or ESXi API at %s on TCP/%s: %s' % (hostname, port, generic_req_exc)))
    except vmodl.fault.InvalidRequest as invalid_request:
        module.fail_json(msg=('Failed to get a response from server %s:%s as request is malformed: %s' % (hostname, port, invalid_request.msg)))
    except Exception as generic_exc:
        module.fail_json(msg=('Unknown error while connecting to vCenter or ESXi API at %s:%s : %s' % (hostname, port, generic_exc)))
    if (service_instance is None):
        module.fail_json(msg=('Unknown error while connecting to vCenter or ESXi API at %s:%s' % (hostname, port)))
    if disconnect_atexit:
        atexit.register(connect.Disconnect, service_instance)
    return service_instance.RetrieveContent()