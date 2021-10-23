def __init__(self, derived_arg_spec, bypass_checks=False, no_log=False, check_invalid_arguments=None, mutually_exclusive=None, required_together=None, required_one_of=None, add_file_common_args=False, supports_check_mode=False, required_if=None, supports_tags=True, facts_module=False, skip_exec=False):
    merged_arg_spec = dict()
    merged_arg_spec.update(AZURE_COMMON_ARGS)
    if supports_tags:
        merged_arg_spec.update(AZURE_TAG_ARGS)
    if derived_arg_spec:
        merged_arg_spec.update(derived_arg_spec)
    merged_required_if = list(AZURE_COMMON_REQUIRED_IF)
    if required_if:
        merged_required_if += required_if
    self.module = AnsibleModule(argument_spec=merged_arg_spec, bypass_checks=bypass_checks, no_log=no_log, check_invalid_arguments=check_invalid_arguments, mutually_exclusive=mutually_exclusive, required_together=required_together, required_one_of=required_one_of, add_file_common_args=add_file_common_args, supports_check_mode=supports_check_mode, required_if=merged_required_if)
    if (not HAS_PACKAGING_VERSION):
        self.fail('Do you have packaging installed? Try `pip install packaging`- {0}'.format(HAS_PACKAGING_VERSION_EXC))
    if (not HAS_MSRESTAZURE):
        self.fail('Do you have msrestazure installed? Try `pip install msrestazure`- {0}'.format(HAS_MSRESTAZURE_EXC))
    if (not HAS_AZURE):
        self.fail("Do you have azure>={1} installed? Try `pip install 'azure>={1}' --upgrade`- {0}".format(HAS_AZURE_EXC, AZURE_MIN_RELEASE))
    self._cloud_environment = None
    self._network_client = None
    self._storage_client = None
    self._resource_client = None
    self._compute_client = None
    self._dns_client = None
    self._web_client = None
    self._containerservice_client = None
    self.check_mode = self.module.check_mode
    self.facts_module = facts_module
    self.credentials = self._get_credentials(self.module.params)
    if (not self.credentials):
        self.fail('Failed to get credentials. Either pass as parameters, set environment variables, or define a profile in ~/.azure/credentials or be logged using AzureCLI.')
    self._cert_validation_mode = (self.module.params['cert_validation_mode'] or self.credentials.get('cert_validation_mode') or os.environ.get('AZURE_CERT_VALIDATION_MODE') or 'validate')
    if (self._cert_validation_mode not in ['validate', 'ignore']):
        self.fail('invalid cert_validation_mode: {0}'.format(self._cert_validation_mode))
    raw_cloud_env = self.credentials.get('cloud_environment')
    if (not raw_cloud_env):
        self._cloud_environment = azure_cloud.AZURE_PUBLIC_CLOUD
    else:
        all_clouds = [x[1] for x in inspect.getmembers(azure_cloud) if isinstance(x[1], azure_cloud.Cloud)]
        matched_clouds = [x for x in all_clouds if (x.name == raw_cloud_env)]
        if (len(matched_clouds) == 1):
            self._cloud_environment = matched_clouds[0]
        elif (len(matched_clouds) > 1):
            self.fail("Azure SDK failure: more than one cloud matched for cloud_environment name '{0}'".format(raw_cloud_env))
        else:
            if (not urlparse.urlparse(raw_cloud_env).scheme):
                self.fail('cloud_environment must be an endpoint discovery URL or one of {0}'.format([x.name for x in all_clouds]))
            try:
                self._cloud_environment = azure_cloud.get_cloud_from_metadata_endpoint(raw_cloud_env)
            except Exception as e:
                self.fail('cloud_environment {0} could not be resolved: {1}'.format(raw_cloud_env, e.message), exception=traceback.format_exc(e))
    if (self.credentials.get('subscription_id', None) is None):
        self.fail('Credentials did not include a subscription_id value.')
    self.log('setting subscription_id')
    self.subscription_id = self.credentials['subscription_id']
    if ((self.credentials.get('client_id') is not None) and (self.credentials.get('secret') is not None) and (self.credentials.get('tenant') is not None)):
        self.azure_credentials = ServicePrincipalCredentials(client_id=self.credentials['client_id'], secret=self.credentials['secret'], tenant=self.credentials['tenant'], cloud_environment=self._cloud_environment, verify=(self._cert_validation_mode == 'validate'))
    elif ((self.credentials.get('ad_user') is not None) and (self.credentials.get('password') is not None)):
        tenant = self.credentials.get('tenant')
        if (not tenant):
            tenant = 'common'
        self.azure_credentials = UserPassCredentials(self.credentials['ad_user'], self.credentials['password'], tenant=tenant, cloud_environment=self._cloud_environment, verify=(self._cert_validation_mode == 'validate'))
    else:
        self.fail('Failed to authenticate with provided credentials. Some attributes were missing. Credentials must include client_id, secret and tenant or ad_user and password or be logged using AzureCLI.')
    if self.module.params.get('tags'):
        self.validate_tags(self.module.params['tags'])
    if (not skip_exec):
        res = self.exec_module(**self.module.params)
        self.module.exit_json(**res)