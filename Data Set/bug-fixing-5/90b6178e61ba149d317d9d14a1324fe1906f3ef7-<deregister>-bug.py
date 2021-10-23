def deregister(self, wait, timeout):
    'De-register the instance from all ELBs and wait for the ELB\n        to report it out-of-service'
    for lb in self.lbs:
        initial_state = self._get_instance_health(lb)
        if (initial_state is None):
            continue
        lb.deregister_instances([self.instance_id])
        self.changed = True
        if wait:
            self._await_elb_instance_state(lb, 'OutOfService', initial_state, timeout)