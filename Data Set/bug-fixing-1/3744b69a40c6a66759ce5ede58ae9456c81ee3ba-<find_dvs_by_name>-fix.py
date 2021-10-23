

def find_dvs_by_name(content, switch_name):
    vmware_distributed_switches = get_all_objs(content, [vim.DistributedVirtualSwitch])
    for dvs in vmware_distributed_switches:
        if (dvs.name == switch_name):
            return dvs
    return None
