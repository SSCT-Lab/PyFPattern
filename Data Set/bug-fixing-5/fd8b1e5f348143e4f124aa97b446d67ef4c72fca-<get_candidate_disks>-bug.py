def get_candidate_disks(self):
    self.debug('getting candidate disks...')
    try:
        (rc, drives_resp) = request((self.api_url + ('/storage-systems/%s/drives' % self.ssid)), method='GET', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs)
    except:
        err = get_exception()
        self.module.exit_json(msg=('Failed to fetch disk drives. Array id [%s].  Error[%s].' % (self.ssid, str(err))))
    try:
        candidate_set = self.filter_drives(drives_resp, exact_drive_count=self.criteria_drive_count, drive_type=self.criteria_drive_type, min_drive_size=self.criteria_drive_min_size, raid_level=self.raid_level, size_unit=self.criteria_size_unit, min_total_capacity=self.criteria_min_usable_capacity, interface_type=self.criteria_drive_interface_type, fde_required=self.criteria_drive_require_fde)
    except:
        err = get_exception()
        self.module.fail_json(msg=('Failed to allocate adequate drive count. Id [%s]. Error [%s].' % (self.ssid, str(err))))
    disk_ids = [d['id'] for d in candidate_set]
    return disk_ids