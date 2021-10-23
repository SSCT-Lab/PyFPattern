def filter_drives(self, drives, interface_type=None, drive_type=None, spindle_speed=None, min_drive_size=None, max_drive_size=None, fde_required=None, size_unit='gb', min_total_capacity=None, min_drive_count=None, exact_drive_count=None, raid_level=None):
    if ((min_total_capacity is None) and (exact_drive_count is None)):
        raise Exception('One of criteria_min_total_capacity or criteria_drive_count must be specified.')
    if min_total_capacity:
        min_total_capacity = (min_total_capacity * self._size_unit_map[size_unit])
    drives = select((lambda d: self._is_valid_drive(d)), drives)
    if interface_type:
        drives = select((lambda d: (d['phyDriveType'] == interface_type)), drives)
    if drive_type:
        drives = select((lambda d: (d['driveMediaType'] == drive_type)), drives)
    if (spindle_speed is not None):
        drives = select((lambda d: (d['spindleSpeed'] == spindle_speed)), drives)
    if min_drive_size:
        min_drive_size_bytes = (min_drive_size * self._size_unit_map[size_unit])
        drives = select((lambda d: (int(d['rawCapacity']) >= min_drive_size_bytes)), drives)
    if max_drive_size:
        max_drive_size_bytes = (max_drive_size * self._size_unit_map[size_unit])
        drives = select((lambda d: (int(d['rawCapacity']) <= max_drive_size_bytes)), drives)
    if fde_required:
        drives = select((lambda d: d['fdeCapable']), drives)
    for (cur_capacity, drives_by_capacity) in GroupBy(drives, (lambda d: int(d['rawCapacity']))):
        for (cur_interface_type, drives_by_interface_type) in GroupBy(drives_by_capacity, (lambda d: d['phyDriveType'])):
            for (cur_drive_type, drives_by_drive_type) in GroupBy(drives_by_interface_type, (lambda d: d['driveMediaType'])):
                drives_by_drive_type = list(drives_by_drive_type)
                candidate_set = list()
                if exact_drive_count:
                    if (len(drives_by_drive_type) < exact_drive_count):
                        continue
                for drive in drives_by_drive_type:
                    candidate_set.append(drive)
                    if self._candidate_set_passes(candidate_set, min_capacity_bytes=min_total_capacity, min_drive_count=min_drive_count, exact_drive_count=exact_drive_count, raid_level=raid_level):
                        return candidate_set
    raise Exception("couldn't find an available set of disks to match specified criteria")