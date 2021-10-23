def migrate_raid_level(self):
    self.debug(("migrating storage pool to raid level '%s'..." % self.raid_level))
    sp_raid_migrate_req = dict(raidLevel=self.raid_level)
    try:
        (rc, resp) = request((self.api_url + ('/storage-systems/%s/storage-pools/%s/raid-type-migration' % (self.ssid, self.name))), data=json.dumps(sp_raid_migrate_req), headers=self.post_headers, method='POST', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
    except:
        err = get_exception()
        pool_id = self.pool_detail['id']
        self.module.exit_json(msg=('Failed to change the raid level of storage pool. Pool id [%s]. Array id [%s].  Error[%s].' % (pool_id, self.ssid, str(err))))