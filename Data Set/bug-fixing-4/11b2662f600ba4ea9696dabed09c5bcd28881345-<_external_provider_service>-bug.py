def _external_provider_service(provider_type, system_service):
    if (provider_type == 'os_image'):
        return (otypes.OpenStackImageProvider, system_service.openstack_image_providers_service())
    elif (provider_type == 'os_network'):
        return (otypes.OpenStackNetworkProvider, system_service.openstack_network_providers_service())
    elif (provider_type == 'os_volume'):
        return (otypes.OpenStackVolumeProvider, system_service.openstack_volume_providers_service())
    elif (provider_type == 'foreman'):
        return (otypes.ExternalHostProvider, system_service.external_host_providers_service())