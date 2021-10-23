

def __target_lun_map(self, storage):
    if storage.get('target'):
        lun_ids = (storage.get('lun_id') if isinstance(storage.get('lun_id'), list) else [storage.get('lun_id')])
        return [(lun_id, storage.get('target')) for lun_id in lun_ids]
    elif storage.get('target_lun_map'):
        return [(target_map.get('lun_id'), target_map.get('target')) for target_map in storage.get('target_lun_map')]
    else:
        lun_ids = (storage.get('lun_id') if isinstance(storage.get('lun_id'), list) else [storage.get('lun_id')])
        return [(lun_id, None) for lun_id in lun_ids]
