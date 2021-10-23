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
                elif self.params['customizations'].get('domain'):
                    guest_map.adapter.dnsDomain = self.params['customizations']['domain']
                if ('dns_servers' in self.params['networks'][network]):
                    guest_map.adapter.dnsServerList = self.params['networks'][network]['dns_servers']
                elif self.params['customizations'].get('dns_servers'):
                    guest_map.adapter.dnsServerList = self.params['customizations']['dns_servers']
                adaptermaps.append(guest_map)
    globalip = vim.vm.customization.GlobalIPSettings()
    globalip.dnsServerList = self.params['customizations']['dns_servers']
    globalip.dnsSuffixList = self.params['customizations'].get(dns_suffix, self.params['customizations']['domain'])
    if self.params['guest_id']:
        guest_id = self.params['guest_id']
    else:
        guest_id = vm_obj.summary.guest.guestId
    if ('windows' in guest_id):
        ident = vim.vm.customization.Sysprep()
        if ('fullname' not in self.params['customizations']):
            self.module.fail_json(msg='You need to define fullname to use Windows customization')
        if ('orgname' not in self.params['customizations']):
            self.module.fail_json(msg='You need to define orgname to use Windows customization')
        ident.userData = vim.vm.customization.UserData()
        ident.userData.computerName = vim.vm.customization.FixedName()
        ident.userData.computerName.name = self.params['customizations'].get(hostname, self.params['name'])
        ident.userData.fullName = str(self.params['customizations']['fullname'])
        ident.userData.orgName = str(self.params['customizations']['orgname'])
        ident.guiUnattended = vim.vm.customization.GuiUnattended()
        ident.guiUnattended.autoLogon = self.params['customizations'].get(autologon, False)
        ident.guiUnattended.autoLogonCount = self.params['customizations'].get(autologoncount, 1)
        ident.identification = vim.vm.customization.Identification()
        if ('password' in self.params['customizations']):
            ident.guiUnattended.password = vim.vm.customization.Password()
            ident.guiUnattended.password.value = str(self.params['customizations']['password'])
            ident.guiUnattended.password.plainText = True
        if ('productid' in self.params['customizations']):
            ident.userData.orgName = str(self.params['customizations']['productid'])
        if ('joindomain' in self.params['customizations']):
            ident.identification.domainadmin = str(self.params['customizations']['domainadmin'])
            ident.identification.domainadminpassword = str(self.params['customizations']['domainadminpassword'])
            ident.identification.joindomain = str(self.params['customizations']['joindomain'])
        elif ('joinworkgroup' in self.params['customizations']):
            ident.identification.joinworkgroup = str(self.params['customizations']['joinworkgroup'])
        if ('runonce' in self.params['customizations']):
            ident.guiRunOnce = vim.vm.customization.GuiRunOnce()
            ident.guiRunOnce.commandList = self.params['customizations']['runonce']
    else:
        ident = vim.vm.customization.LinuxPrep()
        ident.domain = str(self.params['customizations']['domain'])
        ident.hostName = vim.vm.customization.FixedName()
        ident.hostName.name = self.params['customizations'].get(hostname, self.params['name'])
    self.customspec = vim.vm.customization.Specification()
    self.customspec.nicSettingMap = adaptermaps
    self.customspec.globalIPSettings = globalip
    self.customspec.identity = ident