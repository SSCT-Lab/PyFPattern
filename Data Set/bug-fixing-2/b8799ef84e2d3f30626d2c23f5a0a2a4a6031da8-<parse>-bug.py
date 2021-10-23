

def parse(self, inventory, loader, path, cache=False):
    if (self._nmap is None):
        raise AnsibleParserError('nmap inventory plugin requires the nmap cli tool to work')
    super(InventoryModule, self).parse(inventory, loader, path, cache=cache)
    self._read_config_data(path)
    cmd = [self._nmap]
    if (not self._options['ports']):
        cmd.append('-sP')
    if (self._options['ipv4'] and (not self._options['ipv6'])):
        cmd.append('-4')
    elif (self._options['ipv6'] and (not self._options['ipv4'])):
        cmd.append('-6')
    elif ((not self._options['ipv6']) and (not self._options['ipv4'])):
        raise AnsibleParserError('One of ipv4 or ipv6 must be enabled for this plugin')
    if self._options['exclude']:
        cmd.append('--exclude')
        cmd.append(','.join(self._options['exclude']))
    cmd.append(self._options['address'])
    try:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = p.communicate()
        if (p.returncode != 0):
            raise AnsibleParserError(('Failed to run nmap, rc=%s: %s' % (p.returncode, to_native(stderr))))
        host = None
        ip = None
        ports = []
        for line in stdout.splitlines():
            line = to_text(line)
            hits = self.find_host.match(line)
            if hits:
                if (host is not None):
                    self.inventory.set_variable(host, 'ports', ports)
                if hits.group(1).endswith('.in-addr.arpa'):
                    host = hits.group(2)
                else:
                    host = hits.group(1)
                ip = hits.group(2)
                if (host is not None):
                    self.inventory.add_host(host)
                    self.inventory.set_variable(host, 'ip', ip)
                    ports = []
                continue
            host_ports = self.find_port.match(line)
            if ((host is not None) and host_ports):
                ports.append({
                    'port': host_ports.group(1),
                    'protocol': host_ports.group(2),
                    'state': host_ports.group(3),
                    'service': host_ports.group(4),
                })
                continue
        if (host and ports):
            self.inventory.set_variable(host, 'ports', ports)
    except Exception as e:
        raise AnsibleParserError(('failed to parse %s: %s ' % (to_native(path), to_native(e))))
