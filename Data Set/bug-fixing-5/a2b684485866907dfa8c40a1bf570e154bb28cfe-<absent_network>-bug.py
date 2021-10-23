def absent_network(self):
    network = self.get_network()
    if network:
        self.result['changed'] = True
        args = {
            
        }
        args['id'] = network['id']
        if (not self.module.check_mode):
            res = self.cs.deleteNetwork(**args)
            if ('errortext' in res):
                self.module.fail_json(msg=("Failed: '%s'" % res['errortext']))
            poll_async = self.module.params.get('poll_async')
            if (res and poll_async):
                res = self.poll_job(res, 'network')
        return network