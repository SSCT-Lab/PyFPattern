def register_iso(self):
    iso = self.get_iso()
    if (not iso):
        args = {
            
        }
        args['zoneid'] = self.get_zone('id')
        args['domainid'] = self.get_domain('id')
        args['account'] = self.get_account('name')
        args['projectid'] = self.get_project('id')
        args['bootable'] = self.module.params.get('bootable')
        args['ostypeid'] = self.get_os_type('id')
        args['name'] = self.module.params.get('name')
        args['displaytext'] = self.module.params.get('name')
        args['checksum'] = self.module.params.get('checksum')
        args['isdynamicallyscalable'] = self.module.params.get('is_dynamically_scalable')
        args['isfeatured'] = self.module.params.get('is_featured')
        args['ispublic'] = self.module.params.get('is_public')
        if (args['bootable'] and (not args['ostypeid'])):
            self.module.fail_json(msg="OS type 'os_type' is requried if 'bootable=true'.")
        args['url'] = self.module.params.get('url')
        if (not args['url']):
            self.module.fail_json(msg='URL is requried.')
        self.result['changed'] = True
        if (not self.module.check_mode):
            res = self.cs.registerIso(**args)
            iso = res['iso'][0]
    return iso