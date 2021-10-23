def restart_network(self):
    network = self.get_network()
    if (not network):
        self.module.fail_json(msg=("No network named '%s' found." % self.module.params('name')))
    if (network['state'].lower() in ['implemented', 'setup']):
        self.result['changed'] = True
        args = {
            'id': network['id'],
            'cleanup': self.module.params.get('clean_up'),
        }
        if (not self.module.check_mode):
            network = self.cs.restartNetwork(**args)
            if ('errortext' in network):
                self.module.fail_json(msg=("Failed: '%s'" % network['errortext']))
            poll_async = self.module.params.get('poll_async')
            if (network and poll_async):
                network = self.poll_job(network, 'network')
    return network