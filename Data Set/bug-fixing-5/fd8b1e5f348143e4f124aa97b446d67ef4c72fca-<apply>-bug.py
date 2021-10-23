def apply(self):
    changed = False
    pool_exists = False
    self.pool_detail = self.get_storage_pool(self.name)
    if self.pool_detail:
        pool_exists = True
        pool_id = self.pool_detail['id']
        if (self.state == 'absent'):
            self.debug("CHANGED: storage pool exists, but requested state is 'absent'")
            changed = True
        elif (self.state == 'present'):
            if (self.criteria_drive_type and (self.criteria_drive_type != self.pool_detail['driveMediaType'])):
                self.module.fail_json(msg=('drive media type %s cannot be changed to %s' % (self.pool_detail['driveMediaType'], self.criteria_drive_type)))
            if self.needs_expansion:
                self.debug('CHANGED: storage pool needs expansion')
                changed = True
            if self.needs_raid_level_migration:
                self.debug(("CHANGED: raid level migration required; storage pool uses '%s', requested is '%s'" % (self.pool_detail['raidLevel'], self.raid_level)))
                changed = True
    elif (self.state == 'present'):
        self.debug("CHANGED: storage pool does not exist, but requested state is 'present'")
        changed = True
        self.disk_ids = self.get_candidate_disks()
    else:
        self.module.exit_json(msg=('Storage pool [%s] did not exist.' % self.name))
    if (changed and (not self.module.check_mode)):
        if (self.state == 'present'):
            if (not pool_exists):
                self.create_storage_pool()
            else:
                if self.needs_expansion:
                    self.expand_storage_pool()
                if self.remove_drives:
                    self.reduce_drives(self.remove_drives)
                if self.needs_raid_level_migration:
                    self.migrate_raid_level()
                if self.secure_pool:
                    secure_pool_data = dict(securePool=True)
                    try:
                        (retc, r) = request((self.api_url + ('/storage-systems/%s/storage-pools/%s' % (self.ssid, self.pool_detail['id']))), data=json.dumps(secure_pool_data), headers=self.post_headers, method='POST', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120, ignore_errors=True)
                    except:
                        err = get_exception()
                        self.module.exit_json(msg=('Failed to delete storage pool. Pool id [%s]. Array id [%s].  Error[%s].' % (pool_id, self.ssid, str(err))))
                    if (int(retc) == 422):
                        self.module.fail_json(msg='Error in enabling secure pool. One of the drives in the specified storage pool is likely not security capable')
        elif (self.state == 'absent'):
            try:
                remove_vol_opt = ''
                if self.remove_volumes:
                    remove_vol_opt = '?delete-volumes=true'
                (rc, resp) = request((self.api_url + ('/storage-systems/%s/storage-pools/%s%s' % (self.ssid, pool_id, remove_vol_opt))), method='DELETE', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
            except:
                err = get_exception()
                self.module.exit_json(msg=('Failed to delete storage pool. Pool id [%s]. Array id [%s].  Error[%s].' % (pool_id, self.ssid, str(err))))
    self.module.exit_json(changed=changed, **self.pool_detail)