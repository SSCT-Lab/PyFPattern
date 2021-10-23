

def apply_changes(self):
    change_string = self.forti_device.compare_config()
    if change_string:
        self.result['change_string'] = change_string
        self.result['changed'] = True
    if (change_string and (not self.module.check_mode)):
        if self.module.params['file_mode']:
            try:
                f = open(self.module.params['config_file'], 'w')
                f.write(self.candidate_config.to_text())
                f.close
            except IOError:
                e = get_exception()
                self.module.fail_json(msg=('Error writing configuration file. %s' % e))
        else:
            try:
                self.forti_device.commit()
            except FailedCommit:
                self.forti_device.close()
                e = get_exception()
                error_list = self.get_error_infos(e)
                self.module.fail_json(msg_error_list=error_list, msg=('Unable to commit change, check your args, the error was %s' % e.message))
            self.forti_device.close()
    self.module.exit_json(**self.result)
