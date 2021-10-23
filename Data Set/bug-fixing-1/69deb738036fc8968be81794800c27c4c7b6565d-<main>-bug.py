

def main():
    module = AnsibleModule(argument_spec=dict(icmp_block=dict(type='str'), icmp_block_inversion=dict(type='str'), service=dict(type='str'), port=dict(type='str'), rich_rule=dict(type='str'), zone=dict(type='str'), immediate=dict(type='bool', default=False), source=dict(type='str'), permanent=dict(type='bool'), state=dict(type='str', required=True, choices=['absent', 'disabled', 'enabled', 'present']), timeout=dict(type='int', default=0), interface=dict(type='str'), masquerade=dict(type='str'), offline=dict(type='bool')), supports_check_mode=True)
    permanent = module.params['permanent']
    desired_state = module.params['state']
    immediate = module.params['immediate']
    timeout = module.params['timeout']
    interface = module.params['interface']
    masquerade = module.params['masquerade']
    FirewallTransaction.sanity_check(module)
    if ((not permanent) and (not immediate)):
        immediate = True
    if (immediate and fw_offline):
        module.fail_json(msg='firewall is not currently running, unable to perform immediate actions without a running firewall daemon')
    changed = False
    msgs = []
    icmp_block = module.params['icmp_block']
    icmp_block_inversion = module.params['icmp_block_inversion']
    service = module.params['service']
    rich_rule = module.params['rich_rule']
    source = module.params['source']
    zone = module.params['zone']
    if (module.params['port'] is not None):
        (port, protocol) = module.params['port'].strip().split('/')
        if (protocol is None):
            module.fail_json(msg='improper port format (missing protocol?)')
    else:
        port = None
    modification_count = 0
    if (icmp_block is not None):
        modification_count += 1
    if (icmp_block_inversion is not None):
        modification_count += 1
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
        module.fail_json(msg='can only operate on port, service, rich_rule, masquerade, icmp_block, icmp_block_inversion, or interface at once')
    elif ((modification_count > 0) and (desired_state in ['absent', 'present'])):
        module.fail_json(msg='absent and present state can only be used in zone level operations')
    if (icmp_block is not None):
        transaction = IcmpBlockTransaction(module, action_args=(icmp_block, timeout), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
        if (changed is True):
            msgs.append(('Changed icmp-block %s to %s' % (icmp_block, desired_state)))
    if (icmp_block_inversion is not None):
        transaction = IcmpBlockInversionTransaction(module, action_args=(), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
        if (changed is True):
            msgs.append(('Changed icmp-block-inversion %s to %s' % (icmp_block_inversion, desired_state)))
    if (service is not None):
        transaction = ServiceTransaction(module, action_args=(service, timeout), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
        if (changed is True):
            msgs.append(('Changed service %s to %s' % (service, desired_state)))
    if (source is not None):
        transaction = SourceTransaction(module, action_args=(source,), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
    if (port is not None):
        transaction = PortTransaction(module, action_args=(port, protocol, timeout), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
        if (changed is True):
            msgs.append(('Changed port %s to %s' % (('%s/%s' % (port, protocol)), desired_state)))
    if (rich_rule is not None):
        transaction = RichRuleTransaction(module, action_args=(rich_rule, timeout), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
        if (changed is True):
            msgs.append(('Changed rich_rule %s to %s' % (rich_rule, desired_state)))
    if (interface is not None):
        transaction = InterfaceTransaction(module, action_args=(interface,), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
    if (masquerade is not None):
        transaction = MasqueradeTransaction(module, action_args=(), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
    ' If there are no changes within the zone we are operating on the zone itself '
    if ((modification_count == 0) and (desired_state in ['absent', 'present'])):
        transaction = ZoneTransaction(module, action_args=(), zone=zone, desired_state=desired_state, permanent=permanent, immediate=immediate)
        (changed, transaction_msgs) = transaction.run()
        msgs = (msgs + transaction_msgs)
        if (changed is True):
            msgs.append(('Changed zone %s to %s' % (zone, desired_state)))
    if fw_offline:
        msgs.append('(offline operation: only on-disk configs were altered)')
    module.exit_json(changed=changed, msg=', '.join(msgs))
