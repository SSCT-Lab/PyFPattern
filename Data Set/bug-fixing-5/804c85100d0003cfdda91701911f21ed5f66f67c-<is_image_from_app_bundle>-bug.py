def is_image_from_app_bundle(self, obj, sdk_info=None):
    obj_path = obj.name
    if (not obj_path):
        return False
    if obj_path.startswith(APP_BUNDLE_PATHS):
        return True
    if ((SIM_PATH in obj_path) and (SIM_APP_PATH in obj_path)):
        return True
    sdk_name = (sdk_info['sdk_name'].lower() if sdk_info else '')
    if ((sdk_name == 'macos') and (MAC_OS_PATH in obj_path)):
        return True
    if ((sdk_name == 'linux') and (not obj_path.startswith(LINUX_SYS_PATHS))):
        return True
    if ((sdk_name == 'windows') and (not WINDOWS_SYS_PATH.match(obj_path))):
        return True
    return False