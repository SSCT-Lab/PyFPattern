@ensure_connected
def dispatch(self, rpc_command=None, source=None, filter=None):
    "\n        Execute rpc on the remote device eg. dispatch('clear-arp-table')\n        :param rpc_command: specifies rpc command to be dispatched either in plain text or in xml element format (depending on command)\n        :param source: name of the configuration datastore being queried\n        :param filter: specifies the portion of the configuration to retrieve (by default entire configuration is retrieved)\n        :return: Returns xml string containing the RPC response received from remote host\n        "
    if (rpc_command is None):
        raise ValueError('rpc_command value must be provided')
    req = fromstring(rpc_command)
    resp = self.m.dispatch(req, source=source, filter=filter)
    return (resp.data_xml if hasattr(resp, 'data_xml') else resp.xml)