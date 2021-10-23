def get_route_advertisement_status(api, address):
    result = None
    results = api.LocalLB.VirtualAddressV2.get_route_advertisement_state(virtual_addresses=[address])
    if results:
        result = results.pop(0)
        result = result.split('STATE_')[(- 1)].lower()
    return result