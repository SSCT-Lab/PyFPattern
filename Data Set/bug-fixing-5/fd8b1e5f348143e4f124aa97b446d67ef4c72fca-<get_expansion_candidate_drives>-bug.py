def get_expansion_candidate_drives(self):
    if (not self.needs_expansion):
        self.module.fail_json(msg="can't get expansion candidates when pool doesn't need expansion")
    self.debug('fetching expansion candidate drives...')
    try:
        (rc, resp) = request((self.api_url + ('/storage-systems/%s/storage-pools/%s/expand' % (self.ssid, self.pool_detail['id']))), method='GET', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
    except:
        err = get_exception()
        pool_id = self.pool_detail['id']
        self.module.exit_json(msg=('Failed to fetch candidate drives for storage pool. Pool id [%s]. Array id [%s].  Error[%s].' % (pool_id, self.ssid, str(err))))
    current_drive_count = len(self.sp_drives)
    current_capacity_bytes = int(self.pool_detail['totalRaidedSpace'])
    if self.criteria_min_usable_capacity:
        requested_capacity_bytes = (self.criteria_min_usable_capacity * self._size_unit_map[self.criteria_size_unit])
    else:
        requested_capacity_bytes = current_capacity_bytes
    if self.criteria_drive_count:
        minimum_disks_to_add = max((self.criteria_drive_count - current_drive_count), 1)
    else:
        minimum_disks_to_add = 1
    minimum_bytes_to_add = max((requested_capacity_bytes - current_capacity_bytes), 0)
    added_drive_count = 0
    added_capacity_bytes = 0
    drives_to_add = set()
    for s in resp:
        candidate_drives = s['drives']
        if (len(drives_to_add.intersection(candidate_drives)) != 0):
            continue
        drives_to_add.update(candidate_drives)
        added_drive_count += len(candidate_drives)
        added_capacity_bytes += int(s['usableCapacity'])
        if ((added_drive_count >= minimum_disks_to_add) and (added_capacity_bytes >= minimum_bytes_to_add)):
            break
    if ((added_drive_count < minimum_disks_to_add) or (added_capacity_bytes < minimum_bytes_to_add)):
        self.module.fail_json(msg=('unable to find at least %s drives to add that would add at least %s bytes of capacity' % (minimum_disks_to_add, minimum_bytes_to_add)))
    return list(drives_to_add)