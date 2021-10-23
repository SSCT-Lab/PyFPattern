

def _establish_connection(self):
    connection_kwargs = {
        'host': self.vmware_host,
        'user': self.get_option('vmware_user'),
        'pwd': self.get_option('vmware_password'),
        'port': self.get_option('vmware_port'),
    }
    if self.validate_certs:
        connect = SmartConnect
    else:
        if (HAS_URLLIB3 and self.get_option('silence_tls_warnings')):
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        connect = SmartConnectNoSSL
    try:
        self._si = connect(**connection_kwargs)
    except SSLError:
        raise AnsibleError('SSL Error: Certificate verification failed.')
    except gaierror:
        raise AnsibleError(("Connection Error: Unable to connect to '%s'." % to_native(connection_kwargs['host'])))
    except vim.fault.InvalidLogin as e:
        raise AnsibleError(('Connection Login Error: %s' % to_native(e.msg)))
