def _get_body(self, commands, output, reqid=None):
    'Create a valid eAPI JSON-RPC request message\n        '
    if (output not in EAPI_FORMATS):
        msg = ('invalid format, received %s, expected one of %s' % (output, ', '.join(EAPI_FORMATS)))
        self._error(msg=msg)
    params = dict(version=1, cmds=commands, format=output)
    return dict(jsonrpc='2.0', id=reqid, method='runCmds', params=params)