def deploy_vm(self):
    datacenters = get_all_objs(self.content, [vim.Datacenter])
    datacenter = get_obj(self.content, [vim.Datacenter], self.params['datacenter'])
    if (not datacenter):
        self.module.fail_json(msg=('No datacenter named %(datacenter)s was found' % self.params))
    if self.params['folder'].startswith('/'):
        folders = [x for x in self.foldermap['fvim_by_path'].items() if (x[0] == self.params['folder'])]
    else:
        folders = [x for x in self.foldermap['fvim_by_path'].items() if x[0].endswith(self.params['folder'])]
    if (len(folders) == 0):
        self.module.fail_json(msg=('No folder matched the path: %(folder)s' % self.params))
    elif (len(folders) > 1):
        self.module.fail_json(msg=('Too many folders matched "%s", please give the full path starting with /vm/' % self.params['folder']))
    destfolder = folders[0][1]
    hostsystem = self.select_host()
    if self.should_deploy_from_template():
        vm_obj = get_obj(self.content, [vim.VirtualMachine], self.params['template'])
        if (not vm_obj):
            self.module.fail_json(msg=('Could not find a template named %(template)s' % self.params))
    else:
        vm_obj = None
    (datastore, datastore_name) = self.select_datastore(vm_obj)
    resource_pool = self.select_resource_pool(hostsystem)
    self.configspec = vim.vm.ConfigSpec(cpuHotAddEnabled=True, memoryHotAddEnabled=True)
    self.configspec.deviceChange = []
    self.configure_guestid(vm_obj=vm_obj, vm_creation=True)
    self.configure_cpu_and_memory(vm_obj=vm_obj, vm_creation=True)
    self.configure_disks(vm_obj=vm_obj)
    self.configure_network(vm_obj=vm_obj)
    try:
        if self.should_deploy_from_template():
            relospec = vim.vm.RelocateSpec()
            relospec.host = hostsystem
            relospec.datastore = datastore
            relospec.pool = resource_pool
            clonespec = vim.vm.CloneSpec(template=self.params['is_template'], location=relospec)
            if (self.params['customize'] is True):
                clonespec.customization = self.customspec
            clonespec.config = self.configspec
            task = vm_obj.Clone(folder=destfolder, name=self.params['name'], spec=clonespec)
        else:
            self.configspec.name = self.params['name']
            self.configspec.files = vim.vm.FileInfo(logDirectory=None, snapshotDirectory=None, suspendDirectory=None, vmPathName=((('[' + datastore_name) + '] ') + self.params['name']))
            task = destfolder.CreateVM_Task(config=self.configspec, pool=resource_pool)
        self.wait_for_task(task)
    except TypeError:
        self.module.fail_json(msg='TypeError was returned, please ensure to give correct inputs.')
    if (task.info.state == 'error'):
        return {
            'changed': False,
            'failed': True,
            'msg': task.info.error.msg,
        }
    else:
        vm = task.info.result
        if self.params['annotation']:
            annotation_spec = vim.vm.ConfigSpec()
            annotation_spec.annotation = str(self.params['annotation'])
            task = vm.ReconfigVM_Task(annotation_spec)
            self.wait_for_task(task)
        if (self.params['wait_for_ip_address'] or (self.params['state'] in ['poweredon', 'restarted'])):
            self.set_powerstate(vm, 'poweredon', force=False)
            if self.params['wait_for_ip_address']:
                self.wait_for_vm_ip(vm)
        vm_facts = self.gather_facts(vm)
        return {
            'changed': self.change_detected,
            'failed': False,
            'instance': vm_facts,
        }