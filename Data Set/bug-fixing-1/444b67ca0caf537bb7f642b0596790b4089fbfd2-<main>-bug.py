

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(force=dict(required=False, default='no', type='bool'), policy=dict(required=False, default=None, type='json'), name=dict(required=True, type='str'), requester_pays=dict(default='no', type='bool'), s3_url=dict(aliases=['S3_URL'], type='str'), state=dict(default='present', type='str', choices=['present', 'absent']), tags=dict(required=False, default=None, type='dict'), versioning=dict(default=None, type='bool'), ceph=dict(default='no', type='bool')))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    (region, ec2_url, aws_connect_params) = get_aws_connection_info(module)
    if (region in ('us-east-1', '', None)):
        location = Location.DEFAULT
    else:
        location = region
    s3_url = module.params.get('s3_url')
    if ((not s3_url) and ('S3_URL' in os.environ)):
        s3_url = os.environ['S3_URL']
    ceph = module.params.get('ceph')
    if (ceph and (not s3_url)):
        module.fail_json(msg='ceph flavour requires s3_url')
    flavour = 'aws'
    try:
        if (s3_url and ceph):
            ceph = urlparse.urlparse(s3_url)
            connection = boto.connect_s3(host=ceph.hostname, port=ceph.port, is_secure=(ceph.scheme == 'https'), calling_format=OrdinaryCallingFormat(), **aws_connect_params)
            flavour = 'ceph'
        elif is_fakes3(s3_url):
            fakes3 = urlparse.urlparse(s3_url)
            connection = S3Connection(is_secure=(fakes3.scheme == 'fakes3s'), host=fakes3.hostname, port=fakes3.port, calling_format=OrdinaryCallingFormat(), **aws_connect_params)
        elif is_walrus(s3_url):
            walrus = urlparse.urlparse(s3_url).hostname
            connection = boto.connect_walrus(walrus, **aws_connect_params)
        else:
            connection = boto.s3.connect_to_region(location, is_secure=True, calling_format=OrdinaryCallingFormat(), **aws_connect_params)
            if (connection is None):
                connection = boto.connect_s3(**aws_connect_params)
    except boto.exception.NoAuthHandlerFound as e:
        module.fail_json(msg=('No Authentication Handler found: %s ' % str(e)))
    except Exception as e:
        module.fail_json(msg=('Failed to connect to S3: %s' % str(e)))
    if (connection is None):
        module.fail_json(msg='Unknown error, failed to create s3 connection, no information from boto.')
    state = module.params.get('state')
    if (state == 'present'):
        create_or_update_bucket(connection, module, location)
    elif (state == 'absent'):
        destroy_bucket(connection, module, flavour=flavour)
