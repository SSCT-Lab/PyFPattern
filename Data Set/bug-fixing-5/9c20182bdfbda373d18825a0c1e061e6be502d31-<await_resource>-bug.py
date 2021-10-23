def await_resource(conn, resource, status, module):
    wait_timeout = (module.params.get('wait_timeout') + time.time())
    while ((wait_timeout > time.time()) and (resource.status != status)):
        time.sleep(5)
        if (wait_timeout <= time.time()):
            module.fail_json(msg=('Timeout waiting for RDS resource %s' % resource.name))
        if (module.params.get('command') == 'snapshot'):
            if (resource.name is None):
                module.fail_json(msg=('There was a problem waiting for RDS snapshot %s' % resource.snapshot))
            resource = conn.get_db_snapshot(resource.name)
        else:
            if (resource.name is None):
                module.fail_json(msg=('There was a problem waiting for RDS instance %s' % resource.instance))
            resource = conn.get_db_instance(resource.name)
            if (resource is None):
                break
    return resource