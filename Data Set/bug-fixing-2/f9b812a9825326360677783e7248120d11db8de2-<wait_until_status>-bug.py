

def wait_until_status(self, pxname, svname, status):
    '\n        Wait for a service to reach the specified status. Try RETRIES times\n        with INTERVAL seconds of sleep in between. If the service has not reached\n        the expected status in that time, the module will fail. If the service was\n        not found, the module will fail.\n        '
    for i in range(1, self.wait_retries):
        state = self.get_state_for(pxname, svname)
        if (state[0]['status'] == status):
            if ((not self._drain) or ((state[0]['scur'] == '0') and (state == 'MAINT'))):
                return True
        else:
            time.sleep(self.wait_interval)
    self.module.fail_json(msg=("server %s/%s not status '%s' after %d retries. Aborting." % (pxname, svname, status, self.wait_retries)))
