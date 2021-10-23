@property
def is_registered(self):
    '\n            Determine whether the current system\n            Returns:\n              * Boolean - whether the current system is currently registered to\n                          RHSM.\n        '
    if False:
        return (os.path.isfile('/etc/pki/consumer/cert.pem') and os.path.isfile('/etc/pki/consumer/key.pem'))
    args = [SUBMAN_CMD, 'identity']
    (rc, stdout, stderr) = self.module.run_command(args, check_rc=False)
    if (rc == 0):
        return True
    else:
        return False