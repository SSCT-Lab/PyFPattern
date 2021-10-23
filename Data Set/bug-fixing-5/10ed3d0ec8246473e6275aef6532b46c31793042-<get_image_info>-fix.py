def get_image_info(image):
    info = {
        'id': image.ID,
        'name': image.NAME,
        'state': IMAGE_STATES[image.STATE],
        'running_vms': image.RUNNING_VMS,
        'used': bool(image.RUNNING_VMS),
        'user_name': image.UNAME,
        'user_id': image.UID,
        'group_name': image.GNAME,
        'group_id': image.GID,
    }
    return info