def main():
    module = AnsibleModule(argument_spec=dict(autoconnect=dict(required=False, default=None, type='bool'), state=dict(required=True, choices=['present', 'absent'], type='str'), conn_name=dict(required=True, type='str'), master=dict(required=False, default=None, type='str'), ifname=dict(required=False, default=None, type='str'), type=dict(required=False, default=None, choices=['ethernet', 'team', 'team-slave', 'bond', 'bond-slave', 'bridge', 'vlan'], type='str'), ip4=dict(required=False, default=None, type='str'), gw4=dict(required=False, default=None, type='str'), dns4=dict(required=False, default=None, type='list'), ip6=dict(required=False, default=None, type='str'), gw6=dict(required=False, default=None, type='str'), dns6=dict(required=False, default=None, type='str'), mode=dict(require=False, default='balance-rr', type='str', choices=['balance-rr', 'active-backup', 'balance-xor', 'broadcast', '802.3ad', 'balance-tlb', 'balance-alb']), miimon=dict(required=False, default=None, type='str'), downdelay=dict(required=False, default=None, type='str'), updelay=dict(required=False, default=None, type='str'), arp_interval=dict(required=False, default=None, type='str'), arp_ip_target=dict(required=False, default=None, type='str'), mtu=dict(required=False, default=None, type='str'), mac=dict(required=False, default=None, type='str'), stp=dict(required=False, default=True, type='bool'), priority=dict(required=False, default='128', type='str'), slavepriority=dict(required=False, default='32', type='str'), forwarddelay=dict(required=False, default='15', type='str'), hellotime=dict(required=False, default='2', type='str'), maxage=dict(required=False, default='20', type='str'), ageingtime=dict(required=False, default='300', type='str'), vlanid=dict(required=False, default=None, type='str'), vlandev=dict(required=False, default=None, type='str'), flags=dict(required=False, default=None, type='str'), ingress=dict(required=False, default=None, type='str'), egress=dict(required=False, default=None, type='str')), supports_check_mode=True)
    if (not HAVE_DBUS):
        module.fail_json(msg='This module requires dbus python bindings')
    if (not HAVE_NM_CLIENT):
        module.fail_json(msg='This module requires NetworkManager glib API')
    nmcli = Nmcli(module)
    rc = None
    out = ''
    err = ''
    result = {
        
    }
    result['conn_name'] = nmcli.conn_name
    result['state'] = nmcli.state
    if (nmcli.conn_name is None):
        nmcli.module.fail_json(msg="You haven't specified a name for the connection")
    if ((nmcli.type == 'team-slave') and (nmcli.master is None)):
        nmcli.module.fail_json(msg="You haven't specified a name for the master so we're not changing a thing")
    if ((nmcli.type == 'team-slave') and (nmcli.ifname is None)):
        nmcli.module.fail_json(msg="You haven't specified a name for the connection")
    if (nmcli.state == 'absent'):
        if nmcli.connection_exists():
            if module.check_mode:
                module.exit_json(changed=True)
            (rc, out, err) = nmcli.down_connection()
            (rc, out, err) = nmcli.remove_connection()
            if (rc != 0):
                module.fail_json(name=('No Connection named %s exists' % nmcli.conn_name), msg=err, rc=rc)
    elif (nmcli.state == 'present'):
        if nmcli.connection_exists():
            result['Exists'] = 'Connections do exist so we are modifying them'
            if module.check_mode:
                module.exit_json(changed=True)
            (rc, out, err) = nmcli.modify_connection()
        if (not nmcli.connection_exists()):
            result['Connection'] = ('Connection %s of Type %s is being added' % (nmcli.conn_name, nmcli.type))
            if module.check_mode:
                module.exit_json(changed=True)
            (rc, out, err) = nmcli.create_connection()
        if ((rc is not None) and (rc != 0)):
            module.fail_json(name=nmcli.conn_name, msg=err, rc=rc)
    if (rc is None):
        result['changed'] = False
    else:
        result['changed'] = True
    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err
    module.exit_json(**result)