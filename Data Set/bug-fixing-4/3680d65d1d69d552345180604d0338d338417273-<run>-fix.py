def run(self):
    super(ConfigCLI, self).run()
    if self.options.config_file:
        self.config_file = unfrackpath(self.options.config_file, follow=False)
        self.config = ConfigManager(self.config_file)
    else:
        self.config = ConfigManager()
        self.config_file = find_ini_config_file()
    if self.config_file:
        try:
            if (not os.path.exists(self.config_file)):
                raise AnsibleOptionsError(('%s does not exist or is not accessible' % self.config_file))
            elif (not os.path.isfile(self.config_file)):
                raise AnsibleOptionsError(('%s is not a valid file' % self.config_file))
            os.environ['ANSIBLE_CONFIG'] = to_native(self.config_file)
        except:
            if (self.action in ['view']):
                raise
            elif (self.action in ['edit', 'update']):
                display.warning(('File does not exist, used empty file: %s' % self.config_file))
    elif (self.action == 'view'):
        raise AnsibleError('Invalid or no config file was supplied')
    self.execute()