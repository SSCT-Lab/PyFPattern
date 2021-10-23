def get_virtual_gateway_info(virtual_gateway):
    virtual_gateway_info = {
        'VpnGatewayId': virtual_gateway['VpnGatewayId'],
        'State': virtual_gateway['State'],
        'Type': virtual_gateway['Type'],
        'VpcAttachments': virtual_gateway['VpcAttachments'],
        'Tags': virtual_gateway['Tags'],
    }
    return virtual_gateway_info