def customize_vm(self, vm_obj):
    adaptermaps = []
    if (len(self.params['networks']) > 0):
        for network in self.params['networks']:
            if ('ip' in self.params['networks'][network]):
                guest_map = vim.vm.customization.AdapterMapping()
                guest_map.adapter = vim.vm.customization.IPSettings()
                guest_map.adapter.ip = vim.vm.customization.FixedIp()
                guest_map.adapter.ip.ipAddress = str(self.params['networks'][network]['ip'])
                guest_map.adapter.subnetMask = str(self.params['networks'][network]['subnet_mask'])
                if ('gateway' in self.params['networks'][network]):
                    guest_map.adapter.gateway = self.params['networks'][network]['gateway']
                if ('domain' in self.params['networks'][network]):
                    guest_map.adapter.dnsDomain = self.params['networks'][network]['domain']
                elif self.params['customization'].get('domain'):
                    guest_map.adapter.dnsDomain = self.params['customization']['domain']
                if ('dns_servers' in self.params['networks'][network]):
                    guest_map.adapter.dnsServerList = self.params['networks'][network]['dns_servers']
                elif self.params['customization'].get('dns_servers'):
                    guest_map.adapter.dnsServerList = self.params['customization']['dns_servers']
                adaptermaps.append(guest_map)
    globalip = vim.vm.customization.GlobalIPSettings()
    if ('dns_servers' in self.params['customization']):
        globalip.dnsServerList = self.params['customization'].get('dns_servers')
    if (('dns_suffix' in self.params['customization']) or ('domain' in self.params['customization'])):
        globalip.dnsSuffixList = self.params['customization'].get('dns_suffix', self.params['customization']['domain'])
    if self.params['guest_id']:
        guest_id = self.params['guest_id']
    else:
        guest_id = vm_obj.summary.config.guestId
    if ('win' in guest_id):
        ident = vim.vm.customization.Sysprep()
        ident.userData = vim.vm.customization.UserData()
        ident.userData.computerName = vim.vm.customization.FixedName()
        ident.userData.computerName.name = str(self.params['customization'].get('hostname', self.params['name']))
        ident.userData.fullName = str(self.params['customization'].get('fullname', 'Administrator'))
        ident.userData.orgName = str(self.params['customization'].get('orgname', 'ACME'))
        ident.guiUnattended = vim.vm.customization.GuiUnattended()
        ident.guiUnattended.autoLogon = self.params['customization'].get('autologon', False)
        ident.guiUnattended.autoLogonCount = self.params['customization'].get('autologoncount', 1)
        ident.guiUnattended.timeZone = self.params['customization'].get('timezone', 85)
        ident.identification = vim.vm.customization.Identification()
        if (self.params['customization'].get('password', '') != ''):
            ident.guiUnattended.password = vim.vm.customization.Password()
            ident.guiUnattended.password.value = str(self.params['customization']['password'])
            ident.guiUnattended.password.plainText = True
        else:
            self.module.fail_json(msg="The 'customization' section requires 'password' entry, which cannot be empty.")
        if ('productid' in self.params['customization']):
            ident.userData.orgName = str(self.params['customization']['productid'])
        if ('joindomain' in self.params['customization']):
            ident.identification.domainAdmin = str(self.params['customization'].get('domainadmin'))
            ident.identification.domainAdminPassword = str(self.params['customization'].get('domainadminpassword'))
            ident.identification.joinDomain = str(self.params['customization'].get('joindomain'))
        elif ('joinworkgroup' in self.params['customization']):
            ident.identification.joinWorkgroup = str(self.params['customization'].get('joinworkgroup'))
        if ('runonce' in self.params['customization']):
            ident.guiRunOnce = vim.vm.customization.GuiRunOnce()
            ident.guiRunOnce.commandList = self.params['customization']['runonce']
    else:
        ident = vim.vm.customization.LinuxPrep()
        if ('domain' in self.params['customization']):
            ident.domain = str(self.params['customization'].get('domain'))
        ident.hostName = vim.vm.customization.FixedName()
        ident.hostName.name = str(self.params['customization'].get('hostname', self.params['name']))
    self.customspec = vim.vm.customization.Specification()
    self.customspec.nicSettingMap = adaptermaps
    self.customspec.globalIPSettings = globalip
    self.customspec.identity = ident