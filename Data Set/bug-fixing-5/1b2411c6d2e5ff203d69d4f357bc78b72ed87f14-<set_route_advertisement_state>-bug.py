def set_route_advertisement_state(api, destination, partition, route_advertisement_state):
    updated = False
    try:
        state = ('STATE_%s' % route_advertisement_state.strip().upper())
        address = fq_name(partition, destination)
        current_route_advertisement_state = get_route_advertisement_status(api, address)
        if (current_route_advertisement_state != route_advertisement_state):
            api.LocalLB.VirtualAddressV2.set_route_advertisement_state(virtual_addresses=[address], states=[state])
            updated = True
        return updated
    except bigsuds.OperationFailed as e:
        raise Exception(('Error on setting profiles : %s' % e))