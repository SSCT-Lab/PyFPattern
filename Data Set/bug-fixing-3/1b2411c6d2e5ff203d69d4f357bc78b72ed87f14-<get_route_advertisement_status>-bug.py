def get_route_advertisement_status(api, address):
    result = api.LocalLB.VirtualAddressV2.get_route_advertisement_state(virtual_addresses=[address]).pop(0)
    result = result.split('STATE_')[(- 1)].lower()
    return result