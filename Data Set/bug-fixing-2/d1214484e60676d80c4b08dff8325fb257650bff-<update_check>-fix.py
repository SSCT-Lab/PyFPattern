

def update_check(self, entity):

    def check_cpu_pinning():
        if self.param('cpu_pinning'):
            current = []
            if entity.cpu.cpu_tune:
                current = [(str(pin.cpu_set), int(pin.vcpu)) for pin in entity.cpu.cpu_tune.vcpu_pins]
            passed = [(str(pin['cpu']), int(pin['vcpu'])) for pin in self.param('cpu_pinning')]
            return (sorted(current) == sorted(passed))
        return True

    def check_custom_properties():
        if self.param('custom_properties'):
            current = []
            if entity.custom_properties:
                current = [(cp.name, cp.regexp, str(cp.value)) for cp in entity.custom_properties]
            passed = [(cp.get('name'), cp.get('regexp'), str(cp.get('value'))) for cp in self.param('custom_properties') if cp]
            return (sorted(current) == sorted(passed))
        return True
    cpu_mode = getattr(entity.cpu, 'mode')
    vm_display = entity.display
    return (check_cpu_pinning() and check_custom_properties() and (not self.param('cloud_init_persist')) and equal(self.param('cluster'), get_link_name(self._connection, entity.cluster)) and equal(convert_to_bytes(self.param('memory')), entity.memory) and equal(convert_to_bytes(self.param('memory_guaranteed')), entity.memory_policy.guaranteed) and equal(convert_to_bytes(self.param('memory_max')), entity.memory_policy.max) and equal(self.param('cpu_cores'), entity.cpu.topology.cores) and equal(self.param('cpu_sockets'), entity.cpu.topology.sockets) and equal(self.param('cpu_threads'), entity.cpu.topology.threads) and equal(self.param('cpu_mode'), (str(cpu_mode) if cpu_mode else None)) and equal(self.param('type'), str(entity.type)) and equal(self.param('operating_system'), str(entity.os.type)) and equal(self.param('boot_menu'), entity.bios.boot_menu.enabled) and equal(self.param('soundcard_enabled'), entity.soundcard_enabled) and equal(self.param('smartcard_enabled'), getattr(vm_display, 'smartcard_enabled', False)) and equal(self.param('io_threads'), entity.io.threads) and equal(self.param('ballooning_enabled'), entity.memory_policy.ballooning) and equal(self.param('serial_console'), entity.console.enabled) and equal(self.param('usb_support'), entity.usb.enabled) and equal(self.param('sso'), (True if entity.sso.methods else False)) and equal(self.param('quota_id'), getattr(entity.quota, 'id')) and equal(self.param('high_availability'), entity.high_availability.enabled) and equal(self.param('high_availability_priority'), entity.high_availability.priority) and equal(self.param('lease'), get_link_name(self._connection, getattr(entity.lease, 'storage_domain', None))) and equal(self.param('stateless'), entity.stateless) and equal(self.param('cpu_shares'), entity.cpu_shares) and equal(self.param('delete_protected'), entity.delete_protected) and equal(self.param('use_latest_template_version'), entity.use_latest_template_version) and equal(self.param('boot_devices'), [str(dev) for dev in getattr(entity.os.boot, 'devices', [])]) and equal(self.param('instance_type'), get_link_name(self._connection, entity.instance_type), ignore_case=True) and equal(self.param('description'), entity.description) and equal(self.param('comment'), entity.comment) and equal(self.param('timezone'), getattr(entity.time_zone, 'name', None)) and equal(self.param('serial_policy'), str(getattr(entity.serial_number, 'policy', None))) and equal(self.param('serial_policy_value'), getattr(entity.serial_number, 'value', None)) and equal(self.param('placement_policy'), str(entity.placement_policy.affinity)) and equal(self.param('rng_device'), (str(entity.rng_device.source) if entity.rng_device else None)) and (self.param('host') in [self._connection.follow_link(host).name for host in (entity.placement_policy.hosts or [])]))
