@staticmethod
def find_vswitch_by_name(host, vswitch_name):
    '\n        Find and return vSwitch managed object\n        Args:\n            host: Host system managed object\n            vswitch_name: Name of vSwitch to find\n\n        Returns: vSwitch managed object if found, else None\n\n        '
    for vss in host.configManager.networkSystem.networkInfo.vswitch:
        if (vss.name == vswitch_name):
            return vss
    return None