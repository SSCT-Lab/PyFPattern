def check_vswitch_configuration(self):
    "\n        Check if vSwitch exists\n        Returns: 'present' if vSwitch exists or 'absent' if not\n\n        "
    self.vss = self.find_vswitch_by_name(self.host_system, self.switch)
    if (self.vss is None):
        return 'absent'
    else:
        return 'present'