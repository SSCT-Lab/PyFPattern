def _winrm_send_input(self, protocol, shell_id, command_id, stdin, eof=False):
    rq = {
        'env:Envelope': protocol._get_soap_header(resource_uri='http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd', action='http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Send', shell_id=shell_id),
    }
    stream = rq['env:Envelope'].setdefault('env:Body', {
        
    }).setdefault('rsp:Send', {
        
    }).setdefault('rsp:Stream', {
        
    })
    stream['@Name'] = 'stdin'
    stream['@CommandId'] = command_id
    stream['#text'] = base64.b64encode(to_bytes(stdin))
    if eof:
        stream['@End'] = 'true'
    protocol.send_message(xmltodict.unparse(rq))