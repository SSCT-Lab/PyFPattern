def get_to_be_probed_hosts(self, hosts):
    peercmd = [self.glustercmd, 'pool', 'list', '--mode=script']
    (rc, output, err) = self.module.run_command(peercmd, environ_update=self.lang)
    peers_in_cluster = [line.split('\t')[1].strip() for line in filter(None, output.split('\n')[1:])]
    try:
        peers_in_cluster.remove('localhost')
    except ValueError:
        pass
    hosts_to_be_probed = [host for host in hosts if (host not in peers_in_cluster)]
    return hosts_to_be_probed