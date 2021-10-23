

def connect_to_api(module, disconnect_atexit=True):
    hostname = module.params['hostname']
    username = module.params['username']
    password = module.params['password']
    validate_certs = module.params['validate_certs']
    if (validate_certs and (not hasattr(ssl, 'SSLContext'))):
        module.fail_json(msg='pyVim does not support changing verification mode with python < 2.7.9. Either update python or or use validate_certs=false')
    ssl_context = None
    if (not validate_certs):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ssl_context.verify_mode = ssl.CERT_NONE
    service_instance = None
    try:
        service_instance = connect.SmartConnect(host=hostname, user=username, pwd=password, sslContext=ssl_context)
    except vim.fault.InvalidLogin as e:
        module.fail_json(msg=('Unable to log on to vCenter or ESXi API at %s as %s: %s' % (hostname, username, e.msg)))
    except vim.fault.NoPermission as e:
        module.fail_json(msg=('User %s does not have required permission to log on to vCenter or ESXi API at %s: %s' % (username, hostname, e.msg)))
    except (requests.ConnectionError, ssl.SSLError) as e:
        module.fail_json(msg=('Unable to connect to vCenter or ESXi API at %s on TCP/443: %s' % (hostname, e)))
    except Exception as e:
        module.fail_json(msg=('Unknown error connecting to vCenter or ESXi API at %s: %s' % (hostname, e)))
    if (service_instance is None):
        module.fail_json(msg=('Unknown error connecting to vCenter or ESXi API at %s' % hostname))
    if disconnect_atexit:
        atexit.register(connect.Disconnect, service_instance)
    return service_instance.RetrieveContent()
