def customize_vm(self, vm_obj):
    adaptermaps = []
    for network in self.params['networks']:
        guest_map = vim.vm.customization.AdapterMapping()
        guest_map.adapter = vim.vm.customization.IPSettings()
        if (('ip' in network) and ('netmask' in network)):
            guest_map.adapter.ip = vim.vm.customization.FixedIp()
            guest_map.adapter.ip.ipAddress = str(network['ip'])
            guest_map.adapter.subnetMask = str(network['netmask'])
        elif (('type' in network) and (network['type'] == 'dhcp')):
            guest_map.adapter.ip = vim.vm.customization.DhcpIpGenerator()
        if ('gateway' in network):
            guest_map.adapter.gateway = network['gateway']
        if ('domain' in network):
            guest_map.adapter.dnsDomain = network['domain']
        elif ('domain' in self.params['customization']):
            guest_map.adapter.dnsDomain = self.params['customization']['domain']
        if ('dns_servers' in network):
            guest_map.adapter.dnsServerList = network['dns_servers']
        elif ('dns_servers' in self.params['customization']):
            guest_map.adapter.dnsServerList = self.params['customization']['dns_servers']
        adaptermaps.append(guest_map)
    globalip = vim.vm.customization.GlobalIPSettings()
    if ('dns_servers' in self.params['customization']):
        globalip.dnsServerList = self.params['customization']['dns_servers']
    if ('dns_suffix' in self.params['customization']):
        globalip.dnsSuffixList = self.params['customization']['dns_suffix']
    elif ('domain' in self.params['customization']):
        globalip.dnsSuffixList = self.params['customization']['domain']
    if self.params['guest_id']:
        guest_id = self.params['guest_id']
    else:
        guest_id = vm_obj.summary.config.guestId
    if ('win' in guest_id):
        ident = vim.vm.customization.Sysprep()
        ident.userData = vim.vm.customization.UserData()
        ident.userData.computerName = vim.vm.customization.FixedName()
        ident.userData.computerName.name = str(self.params['customization'].get('hostname', self.params['name'].split('.')[0]))
        ident.userData.fullName = str(self.params['customization'].get('fullname', 'Administrator'))
        ident.userData.orgName = str(self.params['customization'].get('orgname', 'ACME'))
        if ('productid' in self.params['customization']):
            ident.userData.productId = str(self.params['customization']['productid'])
        ident.guiUnattended = vim.vm.customization.GuiUnattended()
        if ('autologon' in self.params['customization']):
            ident.guiUnattended.autoLogon = self.params['customization']['autologon']
            ident.guiUnattended.autoLogonCount = self.params['customization'].get('autologoncount', 1)
        if ('timezone' in self.params['customization']):
            ident.guiUnattended.timeZone = self.params['customization']['timezone']
        ident.identification = vim.vm.customization.Identification()
        if (self.params['customization'].get('password', '') != ''):
            ident.guiUnattended.password = vim.vm.customization.Password()
            ident.guiUnattended.password.value = str(self.params['customization']['password'])
            ident.guiUnattended.password.plainText = True
        if ('joindomain' in self.params['customization']):
            if (('domainadmin' not in self.params['customization']) or ('domainadminpassword' not in self.params['customization'])):
                self.module.fail_json(msg="'domainadmin' and 'domainadminpassword' entries are mandatory in 'customization' section to use joindomain feature")
            ident.identification.domainAdmin = str(self.params['customization']['domainadmin'])
            ident.identification.joinDomain = str(self.params['customization']['joindomain'])
            ident.identification.domainAdminPassword = vim.vm.customization.Password()
            ident.identification.domainAdminPassword.value = str(self.params['customization']['domainadminpassword'])
            ident.identification.domainAdminPassword.plainText = True
        elif ('joinworkgroup' in self.params['customization']):
            ident.identification.joinWorkgroup = str(self.params['customization']['joinworkgroup'])
        if ('runonce' in self.params['customization']):
            ident.guiRunOnce = vim.vm.customization.GuiRunOnce()
            ident.guiRunOnce.commandList = self.params['customization']['runonce']
    else:
        ident = vim.vm.customization.LinuxPrep()
        if ('domain' in self.params['customization']):
            ident.domain = str(self.params['customization']['domain'])
        ident.hostName = vim.vm.customization.FixedName()
        hostname = str(self.params['customization'].get('hostname', self.params['name'].split('.')[0]))
        valid_hostname = re.sub('[^a-zA-Z0-9\\-]', '', hostname)
        ident.hostName.name = valid_hostname
    self.customspec = vim.vm.customization.Specification()
    self.customspec.nicSettingMap = adaptermaps
    self.customspec.globalIPSettings = globalip
    self.customspec.identity = ident