def get_aaa_host_info(module, server_type, address):
    aaa_host_info = {
        
    }
    command = 'show run | inc {0}-server.host.{1}'.format(server_type, address)
    body = execute_show_command(command, module, command_type='cli_show_ascii')
    if body[0]:
        try:
            pattern = '(acct-port \\d+)|(timeout \\d+)|(auth-port \\d+)|(key 7 "\\w+")|( port \\d+)'
            raw_match = re.findall(pattern, body[0])
            aaa_host_info = _match_dict(raw_match, {
                'acct-port': 'acct_port',
                'auth-port': 'auth_port',
                'port': 'tacacs_port',
                'timeout': 'host_timeout',
            })
            aaa_host_info['server_type'] = server_type
            aaa_host_info['address'] = address
        except TypeError:
            return {
                
            }
    else:
        return {
            
        }
    return aaa_host_info