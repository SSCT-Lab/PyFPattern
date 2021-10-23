def __init__(self, module):
    self.module = module
    self.state = self.module.params['state']
    self.host = self.module.params['host']
    self.backend = self.module.params['backend']
    self.weight = self.module.params['weight']
    self.socket = self.module.params['socket']
    self.shutdown_sessions = self.module.params['shutdown_sessions']
    self.fail_on_not_found = self.module.params['fail_on_not_found']
    self.wait = self.module.params['wait']
    self.wait_retries = self.module.params['wait_retries']
    self.wait_interval = self.module.params['wait_interval']
    self._drain = self.module.params['drain']
    self.command_results = {
        
    }