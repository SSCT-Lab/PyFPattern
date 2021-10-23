def get_dhcp_options_info(dhcp_option):
    dhcp_option_info = {
        'DhcpOptionsId': dhcp_option['DhcpOptionsId'],
        'DhcpConfigurations': dhcp_option['DhcpConfigurations'],
        'Tags': boto3_tag_list_to_ansible_dict(dhcp_option['Tags']),
    }
    return dhcp_option_info