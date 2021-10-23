

def get_installer_binary(self):
    'Download the LogicMonitor collector installer binary'
    self.module.debug('Running Collector.get_installer_binary...')
    arch = 32
    if self.is_64bits:
        self.module.debug('64 bit system')
        arch = 64
    else:
        self.module.debug('32 bit system')
    if ((self.platform == 'Linux') and (self.id is not None)):
        self.module.debug('Platform is Linux')
        self.module.debug(('Agent ID is ' + str(self.id)))
        installfilepath = (((((self.installdir + '/logicmonitorsetup') + str(self.id)) + '_') + str(arch)) + '.bin')
        self.module.debug(('Looking for existing installer at ' + installfilepath))
        if (not os.path.isfile(installfilepath)):
            self.module.debug('No previous installer found')
            self.module.debug('System changed')
            self.change = True
            if self.check_mode:
                self.exit(changed=True)
            self.module.debug('Downloading installer file')
            self.module.run_command(('mkdir ' + self.installdir))
            try:
                f = open(installfilepath, 'w')
                installer = self.do('logicmonitorsetup', {
                    'id': self.id,
                    'arch': arch,
                })
                f.write(installer)
                f.closed
            except:
                self.fail(msg='Unable to open installer file for writing')
                f.closed
        else:
            self.module.debug('Collector installer already exists')
            return installfilepath
    elif (self.id is None):
        self.fail(msg=((('Error: There is currently no collector ' + 'associated with this device. To download ') + ' the installer, first create a collector ') + 'for this device.'))
    elif (self.platform != 'Linux'):
        self.fail(msg=('Error: LogicMonitor Collector must be ' + 'installed on a Linux device.'))
    else:
        self.fail(msg='Error: Unable  to retrieve the installer from the server')
