def delete_cluster(module, redshift):
    '\n    Delete a cluster.\n\n    module: Ansible module object\n    redshift: authenticated redshift connection object\n    '
    identifier = module.params.get('identifier')
    wait = module.params.get('wait')
    wait_timeout = module.params.get('wait_timeout')
    try:
        redshift.delete_custer(identifier)
    except boto.exception.JSONResponseError as e:
        module.fail_json(msg=str(e))
    if wait:
        try:
            wait_timeout = (time.time() + wait_timeout)
            resource = redshift.describe_clusters(identifier)['DescribeClustersResponse']['DescribeClustersResult']['Clusters'][0]
            while ((wait_timeout > time.time()) and (resource['ClusterStatus'] != 'deleting')):
                time.sleep(5)
                if (wait_timeout <= time.time()):
                    module.fail_json(msg=('Timeout waiting for resource %s' % resource.id))
                resource = redshift.describe_clusters(identifier)['DescribeClustersResponse']['DescribeClustersResult']['Clusters'][0]
        except boto.exception.JSONResponseError as e:
            module.fail_json(msg=str(e))
    return (True, {
        
    })