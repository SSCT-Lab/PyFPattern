def get_rules(meraki, net_id, number):
    path = meraki.construct_path('get_all', net_id=net_id, custom={
        'number': number,
    })
    response = meraki.request(path, method='GET')
    if (meraki.status == 200):
        return response