

def get_ntp_peer(module):
    command = 'show run | inc ntp.(server|peer)'
    ntp_peer_list = []
    ntp = execute_show_command(command, module, command_type='cli_show_ascii')
    if ntp:
        ntp = ntp[0]
        ntp_regex = '.*ntp\\s(server\\s(?P<address>\\S+)|peer\\s(?P<peer_address>\\S+))\\s*((?P<prefer>prefer)\\s*)?(use-vrf\\s(?P<vrf_name>\\S+)\\s*)?(key\\s(?P<key_id>\\d+))?.*'
        split_ntp = ntp.splitlines()
        for peer_line in split_ntp:
            ntp_peer = {
                
            }
            try:
                peer_address = None
                vrf_name = None
                prefer = None
                key_id = None
                match_ntp = re.match(ntp_regex, peer_line, re.DOTALL)
                group_ntp = match_ntp.groupdict()
                address = group_ntp['address']
                peer_address = group_ntp['peer_address']
                prefer = group_ntp['prefer']
                vrf_name = group_ntp['vrf_name']
                key_id = group_ntp['key_id']
                if (prefer is not None):
                    prefer = 'enabled'
                else:
                    prefer = 'disabled'
                if (address is not None):
                    peer_type = 'server'
                elif (peer_address is not None):
                    peer_type = 'peer'
                    address = peer_address
                args = dict(peer_type=peer_type, address=address, prefer=prefer, vrf_name=vrf_name, key_id=key_id)
                ntp_peer = dict(((k, v) for (k, v) in args.items()))
                ntp_peer_list.append(ntp_peer)
            except AttributeError:
                ntp_peer_list = []
    return ntp_peer_list
