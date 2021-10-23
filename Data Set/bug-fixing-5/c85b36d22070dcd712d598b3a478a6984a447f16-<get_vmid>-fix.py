def get_vmid(proxmox, hostname):
    return [vm['vmid'] for vm in proxmox.cluster.resources.get(type='vm') if (('name' in vm) and (vm['name'] == hostname))]