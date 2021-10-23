def get_image_info(image):
    image.info()
    info = {
        'id': image.id,
        'name': image.name,
        'state': IMAGE_STATES[image.state],
        'running_vms': image.running_vms,
        'used': bool(image.running_vms),
        'user_name': image.uname,
        'user_id': image.uid,
        'group_name': image.gname,
        'group_id': image.gid,
    }
    return info