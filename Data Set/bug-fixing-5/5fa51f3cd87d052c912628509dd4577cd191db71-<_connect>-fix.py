def _connect(self):
    if (not HAS_PYPSRP):
        raise AnsibleError(('pypsrp or dependencies are not installed: %s' % to_native(PYPSRP_IMP_ERR)))
    super(Connection, self)._connect()
    self._build_kwargs()
    display.vvv(('ESTABLISH PSRP CONNECTION FOR USER: %s ON PORT %s TO %s' % (self._psrp_user, self._psrp_port, self._psrp_host)), host=self._psrp_host)
    if (not self.runspace):
        connection = WSMan(**self._psrp_conn_kwargs)
        host_ui = PSHostUserInterface()
        self.host = PSHost(None, None, False, 'Ansible PSRP Host', None, host_ui, None)
        self.runspace = RunspacePool(connection, host=self.host, configuration_name=self._psrp_configuration_name)
        display.vvvvv(('PSRP OPEN RUNSPACE: auth=%s configuration=%s endpoint=%s' % (self._psrp_auth, self._psrp_configuration_name, connection.transport.endpoint)), host=self._psrp_host)
        try:
            self.runspace.open()
        except AuthenticationError as e:
            raise AnsibleConnectionFailure(('failed to authenticate with the server: %s' % to_native(e)))
        except WinRMError as e:
            raise AnsibleConnectionFailure(('psrp connection failure during runspace open: %s' % to_native(e)))
        except (ConnectionError, ConnectTimeout) as e:
            raise AnsibleConnectionFailure(('Failed to connect to the host via PSRP: %s' % to_native(e)))
        self._connected = True
    return self