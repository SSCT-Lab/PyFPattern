def __init__(self):
    self.module_arg_spec = dict(resource_group=dict(type='str', updatable=False, disposition='resourceGroupName', required=True), gallery_name=dict(type='str', updatable=False, disposition='galleryName', required=True), gallery_image_name=dict(type='str', updatable=False, disposition='galleryImageName', required=True), name=dict(type='str', updatable=False, disposition='galleryImageVersionName', required=True), location=dict(type='str', updatable=False, disposition='/'), publishing_profile=dict(type='dict', disposition='/properties/publishingProfile', options=dict(target_regions=dict(type='list', disposition='targetRegions', options=dict(name=dict(type='str', required=True), regional_replica_count=dict(type='int', disposition='regionalReplicaCount'), storage_account_type=dict(type='str', disposition='storageAccountType'))), managed_image=dict(type='raw', pattern='/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/images/{name}', disposition='source/managedImage/id'), replica_count=dict(type='int', disposition='replicaCount'), exclude_from_latest=dict(type='bool', disposition='excludeFromLatest'), end_of_life_date=dict(type='str', disposition='endOfLifeDate'), storage_account_type=dict(type='str', disposition='storageAccountType', choices=['Standard_LRS', 'Standard_ZRS']))), state=dict(type='str', default='present', choices=['present', 'absent']))
    self.resource_group = None
    self.gallery_name = None
    self.gallery_image_name = None
    self.name = None
    self.gallery_image_version = None
    self.results = dict(changed=False)
    self.mgmt_client = None
    self.state = None
    self.url = None
    self.status_code = [200, 201, 202]
    self.to_do = Actions.NoAction
    self.body = {
        
    }
    self.query_parameters = {
        
    }
    self.query_parameters['api-version'] = '2019-03-01'
    self.header_parameters = {
        
    }
    self.header_parameters['Content-Type'] = 'application/json; charset=utf-8'
    super(AzureRMGalleryImageVersions, self).__init__(derived_arg_spec=self.module_arg_spec, supports_check_mode=True, supports_tags=True)