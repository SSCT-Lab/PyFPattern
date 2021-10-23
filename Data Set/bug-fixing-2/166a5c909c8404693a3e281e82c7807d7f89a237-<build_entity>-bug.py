

def build_entity(self):
    template = self.__get_template_with_version()
    cluster = self.__get_cluster()
    snapshot = self.__get_snapshot()
    disk_attachments = self.__get_storage_domain_and_all_template_disks(template)
    return otypes.Vm(id=self.param('id'), name=self.param('name'), cluster=(otypes.Cluster(name=cluster) if cluster else None), disk_attachments=disk_attachments, template=(otypes.Template(id=template.id) if template else None), use_latest_template_version=self.param('use_latest_template_version'), stateless=(self.param('stateless') or self.param('use_latest_template_version')), delete_protected=self.param('delete_protected'), bios=(otypes.Bios(boot_menu=otypes.BootMenu(enabled=self.param('boot_menu'))) if (self.param('boot_menu') is not None) else None), console=(otypes.Console(enabled=self.param('serial_console')) if (self.param('serial_console') is not None) else None), usb=(otypes.Usb(enabled=self.param('usb_support')) if (self.param('usb_support') is not None) else None), sso=(otypes.Sso(methods=([otypes.Method(id=otypes.SsoMethod.GUEST_AGENT)] if self.param('sso') else [])) if (self.param('sso') is not None) else None), quota=(otypes.Quota(id=self._module.params.get('quota_id')) if (self.param('quota_id') is not None) else None), high_availability=(otypes.HighAvailability(enabled=self.param('high_availability'), priority=self.param('high_availability_priority')) if ((self.param('high_availability') is not None) or self.param('high_availability_priority')) else None), lease=(otypes.StorageDomainLease(storage_domain=otypes.StorageDomain(id=get_id_by_name(service=self._connection.system_service().storage_domains_service(), name=self.param('lease')))) if (self.param('lease') is not None) else None), cpu=(otypes.Cpu(topology=(otypes.CpuTopology(cores=self.param('cpu_cores'), sockets=self.param('cpu_sockets'), threads=self.param('cpu_threads')) if any((self.param('cpu_cores'), self.param('cpu_sockets'), self.param('cpu_threads'))) else None), cpu_tune=(otypes.CpuTune(vcpu_pins=[otypes.VcpuPin(vcpu=int(pin['vcpu']), cpu_set=str(pin['cpu'])) for pin in self.param('cpu_pinning')]) if self.param('cpu_pinning') else None), mode=(otypes.CpuMode(self.param('cpu_mode')) if self.param('cpu_mode') else None)) if any((self.param('cpu_cores'), self.param('cpu_sockets'), self.param('cpu_threads'), self.param('cpu_mode'), self.param('cpu_pinning'))) else None), cpu_shares=self.param('cpu_shares'), os=(otypes.OperatingSystem(type=self.param('operating_system'), boot=(otypes.Boot(devices=[otypes.BootDevice(dev) for dev in self.param('boot_devices')]) if self.param('boot_devices') else None), cmdline=(self.param('kernel_params') if self.param('kernel_params_persist') else None), initrd=(self.param('initrd_path') if self.param('kernel_params_persist') else None), kernel=(self.param('kernel_path') if self.param('kernel_params_persist') else None)) if (self.param('operating_system') or self.param('boot_devices') or self.param('kernel_params_persist')) else None), type=(otypes.VmType(self.param('type')) if self.param('type') else None), memory=(convert_to_bytes(self.param('memory')) if self.param('memory') else None), memory_policy=(otypes.MemoryPolicy(guaranteed=convert_to_bytes(self.param('memory_guaranteed')), ballooning=self.param('ballooning_enabled'), max=convert_to_bytes(self.param('memory_max'))) if any((self.param('memory_guaranteed'), (self.param('ballooning_enabled') is not None), self.param('memory_max'))) else None), instance_type=(otypes.InstanceType(id=get_id_by_name(self._connection.system_service().instance_types_service(), self.param('instance_type'))) if self.param('instance_type') else None), custom_compatibility_version=(otypes.Version(major=self._get_major(self.param('custom_compatibility_version')), minor=self._get_minor(self.param('custom_compatibility_version'))) if (self.param('custom_compatibility_version') is not None) else None), description=self.param('description'), comment=self.param('comment'), time_zone=(otypes.TimeZone(name=self.param('timezone')) if self.param('timezone') else None), serial_number=(otypes.SerialNumber(policy=otypes.SerialNumberPolicy(self.param('serial_policy')), value=self.param('serial_policy_value')) if ((self.param('serial_policy') is not None) or (self.param('serial_policy_value') is not None)) else None), placement_policy=(otypes.VmPlacementPolicy(affinity=otypes.VmAffinity(self.param('placement_policy')), hosts=([otypes.Host(name=self.param('host'))] if self.param('host') else None)) if self.param('placement_policy') else None), soundcard_enabled=self.param('soundcard_enabled'), display=(otypes.Display(smartcard_enabled=self.param('smartcard_enabled')) if (self.param('smartcard_enabled') is not None) else None), io=(otypes.Io(threads=self.param('io_threads')) if (self.param('io_threads') is not None) else None), numa_tune_mode=(otypes.NumaTuneMode(self.param('numa_tune_mode')) if self.param('numa_tune_mode') else None), rng_device=(otypes.RngDevice(source=otypes.RngSource(self.param('rng_device'))) if self.param('rng_device') else None), custom_properties=([otypes.CustomProperty(name=cp.get('name'), regexp=cp.get('regexp'), value=str(cp.get('value'))) for cp in self.param('custom_properties') if cp] if (self.param('custom_properties') is not None) else None), initialization=(self.get_initialization() if self.param('cloud_init_persist') else None), snapshots=([otypes.Snapshot(id=snapshot.id)] if (snapshot is not None) else None))
