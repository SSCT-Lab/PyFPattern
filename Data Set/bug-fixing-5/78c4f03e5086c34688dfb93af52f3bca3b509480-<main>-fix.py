def main():
    global module
    global module
    module = AnsibleModule(argument_spec=dict(service=dict(required=False, default=None), port=dict(required=False, default=None), rich_rule=dict(required=False, default=None), zone=dict(required=False, default=None), immediate=dict(type='bool', default=False), source=dict(required=False, default=None), permanent=dict(type='bool', required=False, default=None), state=dict(choices=['enabled', 'disabled'], required=True), timeout=dict(type='int', required=False, default=0), interface=dict(required=False, default=None), masquerade=dict(required=False, default=None), offline=dict(type='bool', required=False, default=None)), supports_check_mode=True)
    global fw
    global fw_offline
    global Rich_Rule
    global FirewallClientZoneSettings
    try:
        import firewall.config
        FW_VERSION = firewall.config.VERSION
        from firewall.client import Rich_Rule
        from firewall.client import FirewallClient
        fw = None
        fw_offline = False
        try:
            fw = FirewallClient()
            fw.getDefaultZone()
        except AttributeError:
            from firewall.core.fw_test import Firewall_test
            from firewall.client import FirewallClientZoneSettings
            fw = Firewall_test()
            fw.start()
            fw_offline = True
    except ImportError:
        e = sys.exc_info()[1]
        module.fail_json(msg=('firewalld and its python 2 module are required for this module, version 2.0.11 or newer required (3.0.9 or newer for offline operations) \n %s' % e))
    if fw_offline:
        if (FW_VERSION < '0.3.9'):
            module.fail_json(msg='unsupported version of firewalld, offline operations require >= 3.0.9')
    else:
        if (FW_VERSION < '0.2.11'):
            module.fail_json(msg='unsupported version of firewalld, requires >= 2.0.11')
        try:
            if (fw.connected == False):
                module.fail_json(msg='firewalld service must be running, or try with offline=true')
        except AttributeError:
            module.fail_json(msg=("firewalld connection can't be established,                    installed version (%s) likely too old. Requires firewalld >= 2.0.11" % FW_VERSION))
    if ((module.params['source'] is None) and (module.params['permanent'] is None)):
        module.fail_json(msg='permanent is a required parameter')
    if ((module.params['interface'] is not None) and (module.params['zone'] is None)):
        module.fail(msg='zone is a required parameter')
    if (module.params['immediate'] and fw_offline):
        module.fail(msg='firewall is not currently running, unable to perform immediate actions without a running firewall daemon')
    changed = False
    msgs = []
    service = module.params['service']
    rich_rule = module.params['rich_rule']
    source = module.params['source']
    if (module.params['port'] is not None):
        (port, protocol) = module.params['port'].split('/')
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
    permanent = module.params['permanent']
    desired_state = module.params['state']
    immediate = module.params['immediate']
    timeout = module.params['timeout']
    interface = module.params['interface']
    masquerade = module.params['masquerade']
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
        module.fail_json(msg='can only operate on port, service, rich_rule or interface at once')
    if (service is not None):
        if (immediate and permanent):
            is_enabled_permanent = action_handler(get_service_enabled_permanent, (zone, service))
            is_enabled_immediate = action_handler(get_service_enabled, (zone, service))
            msgs.append('Permanent and Non-Permanent(immediate) operation')
            if (desired_state == 'enabled'):
                if ((not is_enabled_permanent) or (not is_enabled_immediate)):
                    if module.check_mode:
                        module.exit_json(changed=True)
                if (not is_enabled_permanent):
                    action_handler(set_service_enabled_permanent, (zone, service))
                    changed = True
                if (not is_enabled_immediate):
                    action_handler(set_service_enabled, (zone, service, timeout))
                    changed = True
            elif (desired_state == 'disabled'):
                if (is_enabled_permanent or is_enabled_immediate):
                    if module.check_mode:
                        module.exit_json(changed=True)
                if is_enabled_permanent:
                    action_handler(set_service_disabled_permanent, (zone, service))
                    changed = True
                if is_enabled_immediate:
                    action_handler(set_service_disabled, (zone, service))
                    changed = True
        elif (permanent and (not immediate)):
            is_enabled = action_handler(get_service_enabled_permanent, (zone, service))
            msgs.append('Permanent operation')
            if (desired_state == 'enabled'):
                if (is_enabled == False):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_service_enabled_permanent, (zone, service))
                    changed = True
            elif (desired_state == 'disabled'):
                if (is_enabled == True):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_service_disabled_permanent, (zone, service))
                    changed = True
        elif (immediate and (not permanent)):
            is_enabled = action_handler(get_service_enabled, (zone, service))
            msgs.append('Non-permanent operation')
            if (desired_state == 'enabled'):
                if (is_enabled == False):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_service_enabled, (zone, service, timeout))
                    changed = True
            elif (desired_state == 'disabled'):
                if (is_enabled == True):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_service_disabled, (zone, service))
                    changed = True
        if (changed == True):
            msgs.append(('Changed service %s to %s' % (service, desired_state)))
    if (source is not None):
        is_enabled = action_handler(get_source, (zone, source))
        if (desired_state == 'enabled'):
            if (is_enabled == False):
                if module.check_mode:
                    module.exit_json(changed=True)
                action_handler(add_source, (zone, source))
                changed = True
                msgs.append(('Added %s to zone %s' % (source, zone)))
        elif (desired_state == 'disabled'):
            if (is_enabled == True):
                if module.check_mode:
                    module.exit_json(changed=True)
                action_handler(remove_source, (zone, source))
                changed = True
                msgs.append(('Removed %s from zone %s' % (source, zone)))
    if (port is not None):
        if (immediate and permanent):
            is_enabled_permanent = action_handler(get_port_enabled_permanent, (zone, [port, protocol]))
            is_enabled_immediate = action_handler(get_port_enabled, (zone, [port, protocol]))
            msgs.append('Permanent and Non-Permanent(immediate) operation')
            if (desired_state == 'enabled'):
                if ((not is_enabled_permanent) or (not is_enabled_immediate)):
                    if module.check_mode:
                        module.exit_json(changed=True)
                if (not is_enabled_permanent):
                    action_handler(set_port_enabled_permanent, (zone, port, protocol))
                    changed = True
                if (not is_enabled_immediate):
                    action_handler(set_port_enabled, (zone, port, protocol, timeout))
                    changed = True
            elif (desired_state == 'disabled'):
                if (is_enabled_permanent or is_enabled_immediate):
                    if module.check_mode:
                        module.exit_json(changed=True)
                if is_enabled_permanent:
                    action_handler(set_port_disabled_permanent, (zone, port, protocol))
                    changed = True
                if is_enabled_immediate:
                    action_handler(set_port_disabled, (zone, port, protocol))
                    changed = True
        elif (permanent and (not immediate)):
            is_enabled = action_handler(get_port_enabled_permanent, (zone, [port, protocol]))
            msgs.append('Permanent operation')
            if (desired_state == 'enabled'):
                if (is_enabled == False):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_port_enabled_permanent, (zone, port, protocol))
                    changed = True
            elif (desired_state == 'disabled'):
                if (is_enabled == True):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_port_disabled_permanent, (zone, port, protocol))
                    changed = True
        if (immediate and (not permanent)):
            is_enabled = action_handler(get_port_enabled, (zone, [port, protocol]))
            msgs.append('Non-permanent operation')
            if (desired_state == 'enabled'):
                if (is_enabled == False):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_port_enabled, (zone, port, protocol, timeout))
                    changed = True
            elif (desired_state == 'disabled'):
                if (is_enabled == True):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_port_disabled, (zone, port, protocol))
                    changed = True
        if (changed == True):
            msgs.append(('Changed port %s to %s' % (('%s/%s' % (port, protocol)), desired_state)))
    if (rich_rule is not None):
        if (immediate and permanent):
            is_enabled_permanent = action_handler(get_rich_rule_enabled_permanent, (zone, rich_rule))
            is_enabled_immediate = action_handler(get_rich_rule_enabled, (zone, rich_rule))
            msgs.append('Permanent and Non-Permanent(immediate) operation')
            if (desired_state == 'enabled'):
                if ((not is_enabled_permanent) or (not is_enabled_immediate)):
                    if module.check_mode:
                        module.exit_json(changed=True)
                if (not is_enabled_permanent):
                    action_handler(set_rich_rule_enabled_permanent, (zone, rich_rule))
                    changed = True
                if (not is_enabled_immediate):
                    action_handler(set_rich_rule_enabled, (zone, rich_rule, timeout))
                    changed = True
            elif (desired_state == 'disabled'):
                if (is_enabled_permanent or is_enabled_immediate):
                    if module.check_mode:
                        module.exit_json(changed=True)
                if is_enabled_permanent:
                    action_handler(set_rich_rule_disabled_permanent, (zone, rich_rule))
                    changed = True
                if is_enabled_immediate:
                    action_handler(set_rich_rule_disabled, (zone, rich_rule))
                    changed = True
        if (permanent and (not immediate)):
            is_enabled = action_handler(get_rich_rule_enabled_permanent, (zone, rich_rule))
            msgs.append('Permanent operation')
            if (desired_state == 'enabled'):
                if (is_enabled == False):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_rich_rule_enabled_permanent, (zone, rich_rule))
                    changed = True
            elif (desired_state == 'disabled'):
                if (is_enabled == True):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_rich_rule_disabled_permanent, (zone, rich_rule))
                    changed = True
        if (immediate and (not permanent)):
            is_enabled = action_handler(get_rich_rule_enabled, (zone, rich_rule))
            msgs.append('Non-permanent operation')
            if (desired_state == 'enabled'):
                if (is_enabled == False):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_rich_rule_enabled, (zone, rich_rule, timeout))
                    changed = True
            elif (desired_state == 'disabled'):
                if (is_enabled == True):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_rich_rule_disabled, (zone, rich_rule))
                    changed = True
        if (changed == True):
            msgs.append(('Changed rich_rule %s to %s' % (rich_rule, desired_state)))
    if (interface is not None):
        if (immediate and permanent):
            is_enabled_permanent = action_handler(get_interface_permanent, (zone, interface))
            is_enabled_immediate = action_handler(get_interface, (zone, interface))
            msgs.append('Permanent and Non-Permanent(immediate) operation')
            if (desired_state == 'enabled'):
                if ((not is_enabled_permanent) or (not is_enabled_immediate)):
                    if module.check_mode:
                        module.exit_json(changed=True)
                if (not is_enabled_permanent):
                    change_zone_of_interface_permanent(zone, interface)
                    changed = True
                if (not is_enabled_immediate):
                    change_zone_of_interface(zone, interface)
                    changed = True
                if changed:
                    msgs.append(('Changed %s to zone %s' % (interface, zone)))
            elif (desired_state == 'disabled'):
                if (is_enabled_permanent or is_enabled_immediate):
                    if module.check_mode:
                        module.exit_json(changed=True)
                if is_enabled_permanent:
                    remove_interface_permanent(zone, interface)
                    changed = True
                if is_enabled_immediate:
                    remove_interface(zone, interface)
                    changed = True
                if changed:
                    msgs.append(('Removed %s from zone %s' % (interface, zone)))
        elif (permanent and (not immediate)):
            is_enabled = action_handler(get_interface_permanent, (zone, interface))
            msgs.append('Permanent operation')
            if (desired_state == 'enabled'):
                if (is_enabled == False):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    change_zone_of_interface_permanent(zone, interface)
                    changed = True
                    msgs.append(('Changed %s to zone %s' % (interface, zone)))
            elif (desired_state == 'disabled'):
                if (is_enabled == True):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    remove_interface_permanent(zone, interface)
                    changed = True
                    msgs.append(('Removed %s from zone %s' % (interface, zone)))
        elif (immediate and (not permanent)):
            is_enabled = action_handler(get_interface, (zone, interface))
            msgs.append('Non-permanent operation')
            if (desired_state == 'enabled'):
                if (is_enabled == False):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    change_zone_of_interface(zone, interface)
                    changed = True
                    msgs.append(('Changed %s to zone %s' % (interface, zone)))
            elif (desired_state == 'disabled'):
                if (is_enabled == True):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    remove_interface(zone, interface)
                    changed = True
                    msgs.append(('Removed %s from zone %s' % (interface, zone)))
    if (masquerade is not None):
        if (immediate and permanent):
            is_enabled_permanent = action_handler(get_masquerade_enabled_permanent, (zone,))
            is_enabled_immediate = action_handler(get_masquerade_enabled, (zone,))
            msgs.append('Permanent and Non-Permanent(immediate) operation')
            if (desired_state == 'enabled'):
                if ((not is_enabled_permanent) or (not is_enabled_immediate)):
                    if module.check_mode:
                        module.exit_json(changed=True)
                if (not is_enabled_permanent):
                    action_handler(set_masquerade_permanent, (zone, True))
                    changed = True
                if (not is_enabled_immediate):
                    action_handler(set_masquerade_enabled, zone)
                    changed = True
                if changed:
                    msgs.append(('Added masquerade to zone %s' % zone))
            elif (desired_state == 'disabled'):
                if (is_enabled_permanent or is_enabled_immediate):
                    if module.check_mode:
                        module.exit_json(changed=True)
                if is_enabled_permanent:
                    action_handler(set_masquerade_permanent, (zone, False))
                    changed = True
                if is_enabled_immediate:
                    action_handler(set_masquerade_disabled, zone)
                    changed = True
                if changed:
                    msgs.append(('Removed masquerade from zone %s' % zone))
        elif (permanent and (not immediate)):
            is_enabled = action_handler(get_masquerade_enabled_permanent, (zone,))
            msgs.append('Permanent operation')
            if (desired_state == 'enabled'):
                if (is_enabled == False):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_masquerade_permanent, (zone, True))
                    changed = True
                    msgs.append(('Added masquerade to zone %s' % zone))
            elif (desired_state == 'disabled'):
                if (is_enabled == True):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_masquerade_permanent, (zone, False))
                    changed = True
                    msgs.append(('Removed masquerade from zone %s' % zone))
        elif (immediate and (not permanent)):
            is_enabled = action_handler(get_masquerade_enabled, (zone,))
            msgs.append('Non-permanent operation')
            if (desired_state == 'enabled'):
                if (is_enabled == False):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_masquerade_enabled, zone)
                    changed = True
                    msgs.append(('Added masquerade to zone %s' % zone))
            elif (desired_state == 'disabled'):
                if (is_enabled == True):
                    if module.check_mode:
                        module.exit_json(changed=True)
                    action_handler(set_masquerade_disabled, zone)
                    changed = True
                    msgs.append(('Removed masquerade from zone %s' % zone))
    if fw_offline:
        msgs.append('(offline operation: only on-disk configs were altered)')
    module.exit_json(changed=changed, msg=', '.join(msgs))