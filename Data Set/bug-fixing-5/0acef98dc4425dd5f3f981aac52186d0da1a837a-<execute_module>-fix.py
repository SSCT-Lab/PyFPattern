def execute_module(self):
    ' Module execution '
    API = 'v1alpha1'
    KIND = 'UploadTokenRequest'
    self.client = self.get_api_client()
    api_version = 'upload.cdi.kubevirt.io/{0}'.format(API)
    pvc_name = self.params.get('pvc_name')
    pvc_namespace = self.params.get('pvc_namespace')
    upload_host = self.params.get('upload_host')
    upload_host_verify_ssl = self.params.get('upload_host_validate_certs')
    path = self.params.get('path')
    definition = defaultdict(defaultdict)
    definition['kind'] = KIND
    definition['apiVersion'] = api_version
    def_meta = definition['metadata']
    def_meta['name'] = pvc_name
    def_meta['namespace'] = pvc_namespace
    def_spec = definition['spec']
    def_spec['pvcName'] = pvc_name
    imgfile = open(path, 'rb')
    resource = self.find_resource(KIND, api_version, fail=True)
    definition = self.set_defaults(resource, definition)
    result = self.perform_action(resource, definition)
    headers = {
        'Authorization': 'Bearer {0}'.format(result['result']['status']['token']),
    }
    url = '{0}/{1}/upload'.format(upload_host, API)
    ret = requests.post(url, data=imgfile, headers=headers, verify=upload_host_verify_ssl)
    if (ret.status_code != 200):
        self.fail_request('Something went wrong while uploading data', method='POST', url=url, reason=ret.reason, status_code=ret.status_code)
    self.exit_json(changed=True)