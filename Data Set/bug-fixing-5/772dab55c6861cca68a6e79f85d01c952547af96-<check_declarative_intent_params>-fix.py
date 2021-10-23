def check_declarative_intent_params(module, want, result):
    failed_conditions = []
    have_neighbors = None
    for w in want:
        want_state = w.get('state')
        want_tx_rate = w.get('tx_rate')
        want_rx_rate = w.get('rx_rate')
        want_neighbors = w.get('neighbors')
        if ((want_state not in ('up', 'down')) and (not want_tx_rate) and (not want_rx_rate) and (not want_neighbors)):
            continue
        if result['changed']:
            sleep(w['delay'])
        command = ('show interfaces %s' % w['name'])
        (rc, out, err) = exec_command(module, command)
        if (rc != 0):
            module.fail_json(msg=to_text(err, errors='surrogate_then_replace'), command=command, rc=rc)
        if (want_state in ('up', 'down')):
            match = re.search(('%s (\\w+)' % 'line protocol is'), out, re.M)
            have_state = None
            if match:
                have_state = match.group(1)
            if ((have_state is None) or (not conditional(want_state, have_state.strip()))):
                failed_conditions.append(('state ' + ('eq(%s)' % want_state)))
        if want_tx_rate:
            match = re.search(('%s (\\d+)' % 'output rate'), out, re.M)
            have_tx_rate = None
            if match:
                have_tx_rate = match.group(1)
            if ((have_tx_rate is None) or (not conditional(want_tx_rate, have_tx_rate.strip(), cast=int))):
                failed_conditions.append(('tx_rate ' + want_tx_rate))
        if want_rx_rate:
            match = re.search(('%s (\\d+)' % 'input rate'), out, re.M)
            have_rx_rate = None
            if match:
                have_rx_rate = match.group(1)
            if ((have_rx_rate is None) or (not conditional(want_rx_rate, have_rx_rate.strip(), cast=int))):
                failed_conditions.append(('rx_rate ' + want_rx_rate))
        if want_neighbors:
            have_host = []
            have_port = []
            if (have_neighbors is None):
                (rc, have_neighbors, err) = exec_command(module, 'show lldp neighbors detail')
                if (rc != 0):
                    module.fail_json(msg=to_text(err, errors='surrogate_then_replace'), command=command, rc=rc)
            if have_neighbors:
                lines = have_neighbors.strip().split('Local Intf: ')
                for line in lines:
                    field = line.split('\n')
                    if (field[0].strip() == w['name']):
                        for item in field:
                            if item.startswith('System Name:'):
                                have_host.append(item.split(':')[1].strip())
                            if item.startswith('Port Description:'):
                                have_port.append(item.split(':')[1].strip())
            for item in want_neighbors:
                host = item.get('host')
                port = item.get('port')
                if (host and (host not in have_host)):
                    failed_conditions.append(('host ' + host))
                if (port and (port not in have_port)):
                    failed_conditions.append(('port ' + port))
    return failed_conditions