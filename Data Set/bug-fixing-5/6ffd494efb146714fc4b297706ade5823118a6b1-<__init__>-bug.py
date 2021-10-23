def __init__(self, module):
    self.module = module
    self.state = module.params['state']
    self.name = module.params['name']
    self.uid = module.params['uid']
    self.non_unique = module.params['non_unique']
    self.seuser = module.params['seuser']
    self.group = module.params['group']
    self.comment = module.params['comment']
    self.shell = module.params['shell']
    self.password = module.params['password']
    self.force = module.params['force']
    self.remove = module.params['remove']
    self.createhome = module.params['createhome']
    self.move_home = module.params['move_home']
    self.skeleton = module.params['skeleton']
    self.system = module.params['system']
    self.login_class = module.params['login_class']
    self.append = module.params['append']
    self.sshkeygen = module.params['generate_ssh_key']
    self.ssh_bits = module.params['ssh_key_bits']
    self.ssh_type = module.params['ssh_key_type']
    self.ssh_comment = module.params['ssh_key_comment']
    self.ssh_passphrase = module.params['ssh_key_passphrase']
    self.update_password = module.params['update_password']
    self.home = module.params['home']
    self.expires = None
    self.groups = None
    if (module.params['groups'] is not None):
        self.groups = ','.join(module.params['groups'])
    if module.params['expires']:
        try:
            self.expires = time.gmtime(module.params['expires'])
        except Exception:
            e = get_exception()
            module.fail_json(('Invalid expires time %s: %s' % (self.expires, str(e))))
    if (module.params['ssh_key_file'] is not None):
        self.ssh_file = module.params['ssh_key_file']
    else:
        self.ssh_file = os.path.join('.ssh', ('id_%s' % self.ssh_type))