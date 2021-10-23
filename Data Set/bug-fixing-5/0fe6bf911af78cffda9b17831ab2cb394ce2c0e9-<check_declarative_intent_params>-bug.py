def check_declarative_intent_params(module, want):
    failed_conditions = []
    have_neighbors = None
    for w in want:
        want_tx_rate = w.get('tx_rate')
        want_rx_rate = w.get('rx_rate')
        want_neighbors = w.get('neighbors')
        time.sleep(module.params['delay'])
        if w['interface_type']:
            return
        cmd = [{
            'command': 'show interface {0}'.format(w['name']),
            'output': 'text',
        }]
        try:
            out = run_commands(module, cmd, check_rc=False)[0]
        except (AttributeError, IndexError, TypeError):
            out = ''
        if want_tx_rate:
            match = re.search('output rate (\\d+)', out, re.M)
            have_tx_rate = None
            if match:
                have_tx_rate = match.group(1)
            if ((have_tx_rate is None) or (not conditional(want_tx_rate, have_tx_rate.strip(), cast=int))):
                failed_conditions.append(('tx_rate ' + want_tx_rate))
        if want_rx_rate:
            match = re.search('input rate (\\d+)', out, re.M)
            have_rx_rate = None
            if match:
                have_rx_rate = match.group(1)
            if ((have_rx_rate is None) or (not conditional(want_rx_rate, have_rx_rate.strip(), cast=int))):
                failed_conditions.append(('rx_rate ' + want_rx_rate))
        if want_neighbors:
            have_host = []
            have_port = []
            if (have_neighbors is None):
                cmd = [{
                    'command': 'show lldp neighbors interface {0} detail'.format(w['name']),
                    'output': 'text',
                }]
                output = run_commands(module, cmd, check_rc=False)
                if output:
                    have_neighbors = output[0]
                else:
                    have_neighbors = ''
                if (have_neighbors and ('Total entries displayed: 0' not in have_neighbors)):
                    for line in have_neighbors.strip().split('\n'):
                        if line.startswith('Port Description'):
                            have_port.append(line.split(': ')[1])
                        if line.startswith('System Name'):
                            have_host.append(line.split(': ')[1])
            for item in want_neighbors:
                host = item.get('host')
                port = item.get('port')
                if (host and (host not in have_host)):
                    failed_conditions.append(('host ' + host))
                if (port and (port not in have_port)):
                    failed_conditions.append(('port ' + port))
    return failed_conditions