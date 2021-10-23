def read_serverless_config(module):
    path = module.params.get('service_path')
    try:
        with open(os.path.join(path, 'serverless.yml')) as sls_config:
            config = yaml.safe_load(sls_config.read())
            return config
    except IOError as e:
        module.fail_json(msg='Could not open serverless.yml in {}. err: {}'.format(path, str(e)), exception=traceback.format_exc())
    module.fail_json(msg='Failed to open serverless config at {}'.format(os.path.join(path, 'serverless.yml')))