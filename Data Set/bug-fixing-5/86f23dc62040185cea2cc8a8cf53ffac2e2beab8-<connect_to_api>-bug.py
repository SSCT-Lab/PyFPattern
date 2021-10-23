def connect_to_api(module, disconnect_atexit=True):
    hostname = module.params['hostname']
    username = module.params['username']
    password = module.params['password']
    validate_certs = module.params['validate_certs']
    if (validate_certs and (not hasattr(ssl, 'SSLContext'))):
        module.fail_json(msg='pyVim does not support changing verification mode with python < 2.7.9. Either update python or or use validate_certs=false')
    try:
        service_instance = connect.SmartConnect(host=hostname, user=username, pwd=password)
    except vim.fault.InvalidLogin as invalid_login:
        module.fail_json(msg=invalid_login.msg, apierror=str(invalid_login))
    except (requests.ConnectionError, ssl.SSLError) as connection_error:
        if (('[SSL: CERTIFICATE_VERIFY_FAILED]' in str(connection_error)) and (not validate_certs)):
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.verify_mode = ssl.CERT_NONE
            service_instance = connect.SmartConnect(host=hostname, user=username, pwd=password, sslContext=context)
        else:
            module.fail_json(msg='Unable to connect to vCenter or ESXi API on TCP/443.', apierror=str(connection_error))
    except:
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        service_instance = connect.SmartConnect(host=hostname, user=username, pwd=password, sslContext=context)
    if disconnect_atexit:
        atexit.register(connect.Disconnect, service_instance)
    return service_instance.RetrieveContent()