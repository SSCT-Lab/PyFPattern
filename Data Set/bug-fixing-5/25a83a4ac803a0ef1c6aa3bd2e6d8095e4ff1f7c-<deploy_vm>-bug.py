def deploy_vm(self):
    self.folder = self.params.get('folder', None)
    if (self.folder is None):
        self.module.fail_json(msg='Folder is required parameter while deploying new virtual machine')
    if (not self.folder.startswith('/')):
        self.folder = ('/%(folder)s' % self.params)
    self.folder = self.folder.rstrip('/')
    datacenter = self.cache.find_obj(self.content, [vim.Datacenter], self.params['datacenter'])
    if (datacenter is None):
        self.module.fail_json(msg=('No datacenter named %(datacenter)s was found' % self.params))
    dcpath = compile_folder_path_for_object(datacenter)
    if (not dcpath.endswith('/')):
        dcpath += '/'
    if (self.folder.startswith(((dcpath + self.params['datacenter']) + '/vm')) or self.folder.startswith((((dcpath + '/') + self.params['datacenter']) + '/vm'))):
        fullpath = self.folder
    elif (self.folder.startswith('/vm/') or (self.folder == '/vm')):
        fullpath = ('%s%s%s' % (dcpath, self.params['datacenter'], self.folder))
    elif self.folder.startswith('/'):
        fullpath = ('%s%s/vm%s' % (dcpath, self.params['datacenter'], self.folder))
    else:
        fullpath = ('%s%s/vm/%s' % (dcpath, self.params['datacenter'], self.folder))
    f_obj = self.content.searchIndex.FindByInventoryPath(fullpath)
    if (f_obj is None):
        details = {
            'datacenter': datacenter.name,
            'datacenter_path': dcpath,
            'folder': self.folder,
            'full_search_path': fullpath,
        }
        self.module.fail_json(msg=('No folder %s matched in the search path : %s' % (self.folder, fullpath)), details=details)
    destfolder = f_obj
    if self.params['template']:
        vm_obj = self.get_vm_or_template(template_name=self.params['template'])
        if (vm_obj is None):
            self.module.fail_json(msg=('Could not find a template named %(template)s' % self.params))
    else:
        vm_obj = None
    if (self.params['resource_pool'] or self.params['template']):
        resource_pool = self.get_resource_pool()
    (datastore, datastore_name) = self.select_datastore(vm_obj)
    self.configspec = vim.vm.ConfigSpec()
    self.configspec.deviceChange = []
    self.configure_guestid(vm_obj=vm_obj, vm_creation=True)
    self.configure_cpu_and_memory(vm_obj=vm_obj, vm_creation=True)
    self.configure_hardware_params(vm_obj=vm_obj)
    self.configure_resource_alloc_info(vm_obj=vm_obj)
    self.configure_disks(vm_obj=vm_obj)
    self.configure_network(vm_obj=vm_obj)
    self.configure_cdrom(vm_obj=vm_obj)
    network_changes = False
    for nw in self.params['networks']:
        for key in nw:
            if (key not in ('device_type', 'mac', 'name', 'vlan')):
                network_changes = True
                break
    if ((len(self.params['customization']) > 0) or (network_changes is True)):
        self.customize_vm(vm_obj=vm_obj)
    clonespec = None
    clone_method = None
    try:
        if self.params['template']:
            relospec = vim.vm.RelocateSpec()
            if self.params['esxi_hostname']:
                relospec.host = self.select_host()
            relospec.datastore = datastore
            relospec.pool = resource_pool
            if ((self.params['snapshot_src'] is not None) and self.params['linked_clone']):
                relospec.diskMoveType = vim.vm.RelocateSpec.DiskMoveOptions.createNewChildDiskBacking
            clonespec = vim.vm.CloneSpec(template=self.params['is_template'], location=relospec)
            if self.customspec:
                clonespec.customization = self.customspec
            if (self.params['snapshot_src'] is not None):
                snapshot = self.get_snapshots_by_name_recursively(snapshots=vm_obj.snapshot.rootSnapshotList, snapname=self.params['snapshot_src'])
                if (len(snapshot) != 1):
                    self.module.fail_json(msg=('virtual machine "%(template)s" does not contain snapshot named "%(snapshot_src)s"' % self.params))
                clonespec.snapshot = snapshot[0].snapshot
            clonespec.config = self.configspec
            clone_method = 'Clone'
            try:
                task = vm_obj.Clone(folder=destfolder, name=self.params['name'], spec=clonespec)
            except vim.fault.NoPermission as e:
                self.module.fail_json(msg=('Failed to clone virtual machine %s to folder %s due to permission issue: %s' % (self.params['name'], destfolder, to_native(e.msg))))
            self.change_detected = True
        else:
            self.configspec.name = self.params['name']
            self.configspec.files = vim.vm.FileInfo(logDirectory=None, snapshotDirectory=None, suspendDirectory=None, vmPathName=(('[' + datastore_name) + ']'))
            clone_method = 'CreateVM_Task'
            resource_pool = self.get_resource_pool()
            try:
                task = destfolder.CreateVM_Task(config=self.configspec, pool=resource_pool)
            except vmodl.fault.InvalidRequest as e:
                self.module.fail_json(msg=('Failed to create virtual machine due to invalid configuration parameter %s' % to_native(e.msg)))
            except vim.fault.RestrictedVersion as e:
                self.module.fail_json(msg=('Failed to create virtual machine due to product versioning restrictions: %s' % to_native(e.msg)))
            self.change_detected = True
        self.wait_for_task(task)
    except TypeError as e:
        self.module.fail_json(msg=('TypeError was returned, please ensure to give correct inputs. %s' % to_text(e)))
    if (task.info.state == 'error'):
        clonespec_json = serialize_spec(clonespec)
        configspec_json = serialize_spec(self.configspec)
        kwargs = {
            'changed': self.change_detected,
            'failed': True,
            'msg': task.info.error.msg,
            'clonespec': clonespec_json,
            'configspec': configspec_json,
            'clone_method': clone_method,
        }
        return kwargs
    else:
        vm = task.info.result
        if self.params['annotation']:
            annotation_spec = vim.vm.ConfigSpec()
            annotation_spec.annotation = str(self.params['annotation'])
            task = vm.ReconfigVM_Task(annotation_spec)
            self.wait_for_task(task)
        if self.params['customvalues']:
            vm_custom_spec = vim.vm.ConfigSpec()
            self.customize_customvalues(vm_obj=vm, config_spec=vm_custom_spec)
            task = vm.ReconfigVM_Task(vm_custom_spec)
            self.wait_for_task(task)
        if (self.params['wait_for_ip_address'] or (self.params['state'] in ['poweredon', 'restarted'])):
            set_vm_power_state(self.content, vm, 'poweredon', force=False)
            if self.params['wait_for_ip_address']:
                self.wait_for_vm_ip(vm)
        vm_facts = self.gather_facts(vm)
        return {
            'changed': self.change_detected,
            'failed': False,
            'instance': vm_facts,
        }