def checker_ip_range_details(client, module):
    results = client.get_checker_ip_ranges()
    return results