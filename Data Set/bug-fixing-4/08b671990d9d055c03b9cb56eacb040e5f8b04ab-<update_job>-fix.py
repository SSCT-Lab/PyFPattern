def update_job(self):
    try:
        status = self.get_job_status()
        if self.has_config_changed():
            self.result['changed'] = True
            if (not self.module.check_mode):
                self.server.reconfig_job(self.name, self.get_config())
        elif ((status != self.EXCL_STATE) and self.has_state_changed(status)):
            self.result['changed'] = True
            if (not self.module.check_mode):
                self.switch_state()
    except Exception:
        e = get_exception()
        self.module.fail_json(msg=('Unable to reconfigure job, %s for %s' % (str(e), self.jenkins_url)))