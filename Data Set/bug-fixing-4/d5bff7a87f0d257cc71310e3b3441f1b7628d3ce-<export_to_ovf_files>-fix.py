def export_to_ovf_files(self, vm_obj):
    self.create_export_dir(vm_obj=vm_obj)
    export_with_iso = False
    if (('export_with_images' in self.params) and self.params['export_with_images']):
        export_with_iso = True
    if (60 > self.params['download_timeout'] > 10):
        self.download_timeout = self.params['download_timeout']
    ovf_files = []
    http_nfc_lease = vm_obj.ExportVm()
    lease_updater = LeaseProgressUpdater(http_nfc_lease, self.lease_interval)
    total_bytes_written = 0
    total_bytes_to_write = vm_obj.summary.storage.unshared
    if (total_bytes_to_write == 0):
        total_bytes_to_write = vm_obj.summary.storage.committed
        if (total_bytes_to_write == 0):
            http_nfc_lease.HttpNfcLeaseAbort()
            self.module.fail_json(msg='Total storage space occupied by the VM is 0.')
    headers = {
        'Accept': 'application/x-vnd.vmware-streamVmdk',
    }
    cookies = connect.GetStub().cookie
    if cookies:
        headers['Cookie'] = cookies
    lease_updater.start()
    try:
        while True:
            if (http_nfc_lease.state == vim.HttpNfcLease.State.ready):
                for deviceUrl in http_nfc_lease.info.deviceUrl:
                    file_download = False
                    if (deviceUrl.targetId and deviceUrl.disk):
                        file_download = True
                    elif (deviceUrl.url.split('/')[(- 1)].split('.')[(- 1)] == 'iso'):
                        if export_with_iso:
                            file_download = True
                    elif (deviceUrl.url.split('/')[(- 1)].split('.')[(- 1)] == 'nvram'):
                        if self.host_version_at_least(version=(6, 7, 0), vm_obj=vm_obj):
                            file_download = True
                    else:
                        continue
                    device_file_name = deviceUrl.url.split('/')[(- 1)]
                    if (device_file_name.split('.')[0][0:5] == 'disk-'):
                        device_file_name = device_file_name.replace('disk', vm_obj.name)
                    temp_target_disk = os.path.join(self.ovf_dir, device_file_name)
                    device_url = deviceUrl.url
                    if ('*' in device_url):
                        device_url = device_url.replace('*', self.params['hostname'])
                    if file_download:
                        current_bytes_written = self.download_device_files(headers=headers, temp_target_disk=temp_target_disk, device_url=device_url, lease_updater=lease_updater, total_bytes_written=total_bytes_written, total_bytes_to_write=total_bytes_to_write)
                        total_bytes_written += current_bytes_written
                        ovf_file = vim.OvfManager.OvfFile()
                        ovf_file.deviceId = deviceUrl.key
                        ovf_file.path = device_file_name
                        ovf_file.size = current_bytes_written
                        ovf_files.append(ovf_file)
                break
            elif (http_nfc_lease.state == vim.HttpNfcLease.State.initializing):
                sleep(2)
                continue
            elif (http_nfc_lease.state == vim.HttpNfcLease.State.error):
                lease_updater.stop()
                self.module.fail_json(msg=('Get HTTP NFC lease error %s.' % http_nfc_lease.state.error[0].fault))
        ovf_manager = self.content.ovfManager
        ovf_descriptor_name = vm_obj.name
        ovf_parameters = vim.OvfManager.CreateDescriptorParams()
        ovf_parameters.name = ovf_descriptor_name
        ovf_parameters.ovfFiles = ovf_files
        vm_descriptor_result = ovf_manager.CreateDescriptor(obj=vm_obj, cdp=ovf_parameters)
        if vm_descriptor_result.error:
            http_nfc_lease.HttpNfcLeaseAbort()
            lease_updater.stop()
            self.module.fail_json(msg=('Create VM descriptor file error %s.' % vm_descriptor_result.error))
        else:
            vm_descriptor = vm_descriptor_result.ovfDescriptor
            ovf_descriptor_path = os.path.join(self.ovf_dir, (ovf_descriptor_name + '.ovf'))
            sha256_hash = hashlib.sha256()
            with open(self.mf_file, 'a') as mf_handle:
                with open(ovf_descriptor_path, 'wb') as handle:
                    handle.write(vm_descriptor)
                    sha256_hash.update(vm_descriptor)
                mf_handle.write((((('SHA256(' + os.path.basename(ovf_descriptor_path)) + ')= ') + sha256_hash.hexdigest()) + '\n'))
            http_nfc_lease.HttpNfcLeaseProgress(100)
            http_nfc_lease.HttpNfcLeaseComplete()
            lease_updater.stop()
            self.facts.update({
                'manifest': self.mf_file,
                'ovf_file': ovf_descriptor_path,
            })
    except Exception as err:
        kwargs = {
            'changed': False,
            'failed': True,
            'msg': to_text(err),
        }
        http_nfc_lease.HttpNfcLeaseAbort()
        lease_updater.stop()
        return kwargs
    return {
        'changed': True,
        'failed': False,
        'instance': self.facts,
    }