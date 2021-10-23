def get_netstream_config(self):
    'get current netstream configuration'
    cmd = 'display current-configuration | include ^netstream export'
    (rc, out, err) = exec_command(self.module, cmd)
    if (rc != 0):
        self.module.fail_json(msg=err)
    config = str(out).strip()
    return config