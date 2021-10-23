def await_resource(conn, resource, status, module):
    start_time = time.time()
    wait_timeout = (module.params.get('wait_timeout') + start_time)
    check_interval = 5
    while ((wait_timeout > time.time()) and (resource.status != status)):
        time.sleep(check_interval)
        if (wait_timeout <= time.time()):
            module.fail_json(msg=('Timeout waiting for RDS resource %s' % resource.name))
        if (module.params.get('command') == 'snapshot'):
            if (resource.name is None):
                module.fail_json(msg=('There was a problem waiting for RDS snapshot %s' % resource.snapshot))
            resource = AWSRetry.backoff(tries=5, delay=20, backoff=1.5)(conn.get_db_snapshot)(resource.name)
        else:
            if (resource.name is None):
                module.fail_json(msg=('There was a problem waiting for RDS instance %s' % resource.instance))
            resource = AWSRetry.backoff(tries=5, delay=20, backoff=1.5)(conn.get_db_instance)(resource.name)
            if (resource is None):
                break
        if (time.time() > (start_time + 90)):
            check_interval = 20
    return resource