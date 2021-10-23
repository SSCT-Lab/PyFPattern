

def mysql_connect(module, login_user=None, login_password=None, config_file='', ssl_cert=None, ssl_key=None, ssl_ca=None, db=None, cursor_class=None, connect_timeout=30):
    config = {
        
    }
    if ((ssl_ca is not None) or (ssl_key is not None) or (ssl_cert is not None)):
        config['ssl'] = {
            
        }
    if module.params['login_unix_socket']:
        config['unix_socket'] = module.params['login_unix_socket']
    else:
        config['host'] = module.params['login_host']
        config['port'] = module.params['login_port']
    if os.path.exists(config_file):
        config['read_default_file'] = config_file
    if (login_user is not None):
        config['user'] = login_user
    if (login_password is not None):
        config['passwd'] = login_password
    if (ssl_cert is not None):
        config['ssl']['cert'] = ssl_cert
    if (ssl_key is not None):
        config['ssl']['key'] = ssl_key
    if (ssl_ca is not None):
        config['ssl']['ca'] = ssl_ca
    if (db is not None):
        config['db'] = db
    if (connect_timeout is not None):
        config['connect_timeout'] = connect_timeout
    db_connection = MySQLdb.connect(**config)
    if (cursor_class is not None):
        return db_connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    else:
        return db_connection.cursor()
