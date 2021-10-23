

def main():
    module = AnsibleModule(argument_spec=dict(login_user=dict(type='str'), login_password=dict(type='str', no_log=True), login_host=dict(type='str', default='localhost'), login_port=dict(type='int', default=3306), login_unix_socket=dict(type='str'), mode=dict(type='str', default='getslave', choices=['getmaster', 'getslave', 'changemaster', 'stopslave', 'startslave', 'resetslave', 'resetslaveall']), master_auto_position=dict(type='bool', default=False), master_host=dict(type='str'), master_user=dict(type='str'), master_password=dict(type='str', no_log=True), master_port=dict(type='int'), master_connect_retry=dict(type='int'), master_log_file=dict(type='str'), master_log_pos=dict(type='int'), relay_log_file=dict(type='str'), relay_log_pos=dict(type='int'), master_ssl=dict(type='bool', default=False), master_ssl_ca=dict(type='str'), master_ssl_capath=dict(type='str'), master_ssl_cert=dict(type='str'), master_ssl_key=dict(type='str'), master_ssl_cipher=dict(type='str'), connect_timeout=dict(type='int', default=30), config_file=dict(type='path', default='~/.my.cnf'), client_cert=dict(type='path', aliases=['ssl_cert']), client_key=dict(type='path', aliases=['ssl_key']), ca_cert=dict(type='path', aliases=['ssl_ca']), master_use_gtid=dict(type='str', choices=['current_pos', 'slave_pos', 'disabled']), master_delay=dict(type='int')))
    mode = module.params['mode']
    master_host = module.params['master_host']
    master_user = module.params['master_user']
    master_password = module.params['master_password']
    master_port = module.params['master_port']
    master_connect_retry = module.params['master_connect_retry']
    master_log_file = module.params['master_log_file']
    master_log_pos = module.params['master_log_pos']
    relay_log_file = module.params['relay_log_file']
    relay_log_pos = module.params['relay_log_pos']
    master_ssl = module.params['master_ssl']
    master_ssl_ca = module.params['master_ssl_ca']
    master_ssl_capath = module.params['master_ssl_capath']
    master_ssl_cert = module.params['master_ssl_cert']
    master_ssl_key = module.params['master_ssl_key']
    master_ssl_cipher = module.params['master_ssl_cipher']
    master_auto_position = module.params['master_auto_position']
    ssl_cert = module.params['client_cert']
    ssl_key = module.params['client_key']
    ssl_ca = module.params['ca_cert']
    connect_timeout = module.params['connect_timeout']
    config_file = module.params['config_file']
    master_delay = module.params['master_delay']
    if (module.params.get('master_use_gtid') == 'disabled'):
        master_use_gtid = 'no'
    else:
        master_use_gtid = module.params['master_use_gtid']
    if (mysql_driver is None):
        module.fail_json(msg=mysql_driver_fail_msg)
    else:
        warnings.filterwarnings('error', category=mysql_driver.Warning)
    login_password = module.params['login_password']
    login_user = module.params['login_user']
    try:
        cursor = mysql_connect(module, login_user, login_password, config_file, ssl_cert, ssl_key, ssl_ca, None, cursor_class='DictCursor', connect_timeout=connect_timeout)
    except Exception as e:
        if os.path.exists(config_file):
            module.fail_json(msg=('unable to connect to database, check login_user and login_password are correct or %s has the credentials. Exception message: %s' % (config_file, to_native(e))))
        else:
            module.fail_json(msg=('unable to find %s. Exception message: %s' % (config_file, to_native(e))))
    if (mode in 'getmaster'):
        status = get_master_status(cursor)
        if (not isinstance(status, dict)):
            status = dict(Is_Master=False, msg='Server is not configured as mysql master')
        else:
            status['Is_Master'] = True
        module.exit_json(queries=executed_queries, **status)
    elif (mode in 'getslave'):
        status = get_slave_status(cursor)
        if (not isinstance(status, dict)):
            status = dict(Is_Slave=False, msg='Server is not configured as mysql slave')
        else:
            status['Is_Slave'] = True
        module.exit_json(queries=executed_queries, **status)
    elif (mode in 'changemaster'):
        chm = []
        result = {
            
        }
        if master_host:
            chm.append(("MASTER_HOST='%s'" % master_host))
        if master_user:
            chm.append(("MASTER_USER='%s'" % master_user))
        if master_password:
            chm.append(("MASTER_PASSWORD='%s'" % master_password))
        if (master_port is not None):
            chm.append(('MASTER_PORT=%s' % master_port))
        if (master_connect_retry is not None):
            chm.append(('MASTER_CONNECT_RETRY=%s' % master_connect_retry))
        if master_log_file:
            chm.append(("MASTER_LOG_FILE='%s'" % master_log_file))
        if (master_log_pos is not None):
            chm.append(('MASTER_LOG_POS=%s' % master_log_pos))
        if master_delay:
            chm.append(('MASTER_DELAY=%s' % master_delay))
        if relay_log_file:
            chm.append(("RELAY_LOG_FILE='%s'" % relay_log_file))
        if (relay_log_pos is not None):
            chm.append(('RELAY_LOG_POS=%s' % relay_log_pos))
        if master_ssl:
            chm.append('MASTER_SSL=1')
        if master_ssl_ca:
            chm.append(("MASTER_SSL_CA='%s'" % master_ssl_ca))
        if master_ssl_capath:
            chm.append(("MASTER_SSL_CAPATH='%s'" % master_ssl_capath))
        if master_ssl_cert:
            chm.append(("MASTER_SSL_CERT='%s'" % master_ssl_cert))
        if master_ssl_key:
            chm.append(("MASTER_SSL_KEY='%s'" % master_ssl_key))
        if master_ssl_cipher:
            chm.append(("MASTER_SSL_CIPHER='%s'" % master_ssl_cipher))
        if master_auto_position:
            chm.append('MASTER_AUTO_POSITION=1')
        if (master_use_gtid is not None):
            chm.append(('MASTER_USE_GTID=%s' % master_use_gtid))
        try:
            changemaster(cursor, chm)
        except mysql_driver.Warning as e:
            result['warning'] = to_native(e)
        except Exception as e:
            module.fail_json(msg=('%s. Query == CHANGE MASTER TO %s' % (to_native(e), chm)))
        result['changed'] = True
        module.exit_json(queries=executed_queries, **result)
    elif (mode in 'startslave'):
        started = start_slave(cursor)
        if (started is True):
            module.exit_json(msg='Slave started ', changed=True, queries=executed_queries)
        else:
            module.exit_json(msg='Slave already started (Or cannot be started)', changed=False, queries=executed_queries)
    elif (mode in 'stopslave'):
        stopped = stop_slave(cursor)
        if (stopped is True):
            module.exit_json(msg='Slave stopped', changed=True, queries=executed_queries)
        else:
            module.exit_json(msg='Slave already stopped', changed=False, queries=executed_queries)
    elif (mode in 'resetslave'):
        reset = reset_slave(cursor)
        if (reset is True):
            module.exit_json(msg='Slave reset', changed=True, queries=executed_queries)
        else:
            module.exit_json(msg='Slave already reset', changed=False, queries=executed_queries)
    elif (mode in 'resetslaveall'):
        reset = reset_slave_all(cursor)
        if (reset is True):
            module.exit_json(msg='Slave reset', changed=True, queries=executed_queries)
        else:
            module.exit_json(msg='Slave already reset', changed=False, queries=executed_queries)
    warnings.simplefilter('ignore')
