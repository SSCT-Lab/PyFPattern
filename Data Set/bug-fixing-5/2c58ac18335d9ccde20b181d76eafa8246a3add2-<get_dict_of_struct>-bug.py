def get_dict_of_struct(connection, vm):
    '\n    Transform SDK Vm Struct type to Python dictionary.\n    '
    if (vm is None):
        return dict()
    vms_service = connection.system_service().vms_service()
    clusters_service = connection.system_service().clusters_service()
    vm_service = vms_service.vm_service(vm.id)
    devices = vm_service.reported_devices_service().list()
    tags = vm_service.tags_service().list()
    stats = vm_service.statistics_service().list()
    labels = vm_service.affinity_labels_service().list()
    groups = clusters_service.cluster_service(vm.cluster.id).affinity_groups_service().list()
    return {
        'id': vm.id,
        'name': vm.name,
        'host': (connection.follow_link(vm.host).name if vm.host else None),
        'cluster': connection.follow_link(vm.cluster).name,
        'status': str(vm.status),
        'description': vm.description,
        'fqdn': vm.fqdn,
        'os_type': vm.os.type,
        'template': connection.follow_link(vm.template).name,
        'tags': [tag.name for tag in tags],
        'affinity_labels': [label.name for label in labels],
        'affinity_groups': [group.name for group in groups if (vm.name in [vm.name for vm in connection.follow_link(group.vms)])],
        'statistics': dict(((stat.name, stat.values[0].datum) for stat in stats)),
        'devices': dict(((device.name, [ip.address for ip in device.ips]) for device in devices)),
        'ansible_host': (devices[0].ips[0].address if (len(devices) > 0) else None),
    }