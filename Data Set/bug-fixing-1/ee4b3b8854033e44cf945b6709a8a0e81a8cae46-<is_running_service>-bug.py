

def is_running_service(service_status):
    return (service_status['ActiveState'] in set(['active', 'activating', 'deactivating']))
