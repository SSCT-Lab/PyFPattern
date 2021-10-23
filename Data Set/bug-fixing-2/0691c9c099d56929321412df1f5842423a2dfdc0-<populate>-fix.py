

def populate(self, collected_facts=None):
    hardware_facts = {
        
    }
    self.module.run_command_environ_update = {
        'LANG': 'C',
        'LC_ALL': 'C',
        'LC_NUMERIC': 'C',
    }
    cpu_facts = self.get_cpu_facts(collected_facts=collected_facts)
    memory_facts = self.get_memory_facts()
    dmi_facts = self.get_dmi_facts()
    device_facts = self.get_device_facts()
    uptime_facts = self.get_uptime_facts()
    lvm_facts = self.get_lvm_facts()
    mount_facts = {
        
    }
    try:
        mount_facts = self.get_mount_facts()
    except timeout.TimeoutError:
        pass
    hardware_facts.update(cpu_facts)
    hardware_facts.update(memory_facts)
    hardware_facts.update(dmi_facts)
    hardware_facts.update(device_facts)
    hardware_facts.update(uptime_facts)
    hardware_facts.update(lvm_facts)
    hardware_facts.update(mount_facts)
    return hardware_facts
