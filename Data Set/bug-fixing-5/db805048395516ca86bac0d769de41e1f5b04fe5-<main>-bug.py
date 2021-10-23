def main():
    global module
    module = AnsibleModule(argument_spec=dict(service=dict(required=False, default=None), port=dict(required=False, default=None), rich_rule=dict(required=False, default=None), zone=dict(required=False, default=None), immediate=dict(type='bool', default=False), source=dict(required=False, default=None), permanent=dict(type='bool', required=False, default=None), state=dict(choices=['enabled', 'disabled', 'present', 'absent'], required=True), timeout=dict(type='int', required=False, default=0), interface=dict(required=False, default=None), masquerade=dict(required=False, default=None), offline=dict(type='bool', required=False, default=None)), supports_check_mode=True)
    if fw_offline:
        if (FW_VERSION < '0.3.9'):
            module.fail_json(msg='unsupported version of firewalld, offline operations require >= 0.3.9')
    else:
        if (FW_VERSION < '0.2.11'):
            module.fail_json(msg='unsupported version of firewalld, requires >= 0.2.11')
        try:
            if (fw.connected is False):
                module.fail_json(msg='firewalld service must be running, or try with offline=true')
        except AttributeError:
            module.fail_json(msg=("firewalld connection can't be established,                    installed version (%s) likely too old. Requires firewalld >= 0.2.11" % FW_VERSION))
    if import_failure:
        module.fail_json(msg='firewalld and its python module are required for this module, version 0.2.11 or newer required (0.3.9 or newer for offline operations)')
    permanent = module.params['permanent']
    desired_state = module.params['state']
    immediate = module.params['immediate']
    timeout = module.params['timeout']
    interface = module.params['interface']
    masquerade = module.params['masquerade']
    if ((not permanent) and (not immediate)):
        immediate = True
    if (immediate and fw_offline):
        module.fail(msg='firewall is not currently running, unable to perform immediate actions without a running firewall daemon')
    changed = False
    msgs = []
    service = module.params['service']
    rich_rule = module.params['rich_rule']
    source = module.params['source']
    if (module.params['port'] is not None):
        (port, protocol) = module.params['port'].strip().split('/')
        if (protocol is None):
            module.fail_json(msg='improper port format (missing protocol?)')
    else:
        port = None
    if (module.params['zone'] is not None):
        zone = module.params['zone']
    elif fw_offline:
        zone = fw.get_default_zone()
    else:
        zone = fw.getDefaultZone()
    modification_count = 0
    if (service is not None):
        modification_count += 1
    if (port is not None):
        modification_count += 1
    if (rich_rule is not None):
        modification_count += 1
    if (interface is not None):
        modification_count += 1
    if (masquerade is not None):
        modification_count += 1
    if (modification_count > 1):
        module.fail_json(msg='can only operate on port, service, rich_rule, or interface at once')
    elif ((modification_count > 0) and (desired_state in ['absent', 'present'])):
        module.fail_json(msg='absent and present state can only be used in zone level operations')
    if (service is not None):
        transaction = ServiceTransaction(fw, action_args=(service, timeout), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate, fw_offline=fw_offline)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
        if (changed is True):
            msgs.append(('Changed service %s to %s' % (service, desired_state)))
    if (source is not None):
        transaction = SourceTransaction(fw, action_args=(source,), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate, fw_offline=fw_offline)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
    if (port is not None):
        transaction = PortTransaction(fw, action_args=(port, protocol, timeout), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate, fw_offline=fw_offline)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
        if (changed is True):
            msgs.append(('Changed port %s to %s' % (('%s/%s' % (port, protocol)), desired_state)))
    if (rich_rule is not None):
        transaction = RichRuleTransaction(fw, action_args=(rich_rule, timeout), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate, fw_offline=fw_offline)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
        if (changed is True):
            msgs.append(('Changed rich_rule %s to %s' % (rich_rule, desired_state)))
    if (interface is not None):
        transaction = InterfaceTransaction(fw, action_args=(interface,), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate, fw_offline=fw_offline)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
    if (masquerade is not None):
        transaction = MasqueradeTransaction(fw, action_args=(), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate, fw_offline=fw_offline)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
    ' If there are no changes within the zone we are operating on the zone itself '
    if ((modification_count == 0) and (desired_state in ['absent', 'present'])):
        transaction = ZoneTransaction(fw, action_args=(), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate, fw_offline=fw_offline)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
        if (changed is True):
            msgs.append(('Changed zone %s to %s' % (zone, desired_state)))
    if fw_offline:
        msgs.append('(offline operation: only on-disk configs were altered)')
    module.exit_json(changed=changed, msg=', '.join(msgs))