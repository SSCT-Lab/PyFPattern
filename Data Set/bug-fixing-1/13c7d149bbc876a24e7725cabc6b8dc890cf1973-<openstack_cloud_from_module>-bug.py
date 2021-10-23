

def openstack_cloud_from_module(module, min_version='0.12.0'):
    from distutils.version import StrictVersion
    try:
        import importlib
        sdk = importlib.import_module('openstack')
    except ImportError:
        module.fail_json(msg='openstacksdk is required for this module')
    if min_version:
        if (StrictVersion(sdk.version.__version__) < StrictVersion(min_version)):
            module.fail_json(msg='To utilize this module, the installed version ofthe openstacksdk library MUST be >={min_version}'.format(min_version=min_version))
    cloud_config = module.params.pop('cloud', None)
    try:
        if isinstance(cloud_config, dict):
            fail_message = 'A cloud config dict was provided to the cloud parameter but also a value was provided for {param}. If a cloud config dict is provided, {param} should be excluded.'
            for param in ('auth', 'region_name', 'verify', 'cacert', 'key', 'api_timeout', 'interface'):
                if (module.params[param] is not None):
                    module.fail_json(fail_message.format(param=param))
            if (module.params['auth_type'] != 'password'):
                module.fail_json(fail_message.format(param='auth_type'))
            return (sdk, sdk.connect(**cloud_config))
        else:
            return (sdk, sdk.connect(cloud=cloud_config, auth_type=module.params['auth_type'], auth=module.params['auth'], region_name=module.params['region_name'], verify=module.params['verify'], cacert=module.params['cacert'], key=module.params['key'], api_timeout=module.params['api_timeout'], interface=module.params['interface']))
    except sdk.exceptions.SDKException as e:
        module.fail_json(msg=str(e))
