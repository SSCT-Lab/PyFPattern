

def _get_mount_size_facts(self, mountpoint):
    size_total = None
    size_available = None
    try:
        statvfs_result = os.statvfs(mountpoint)
        size_total = (statvfs_result.f_frsize * statvfs_result.f_blocks)
        size_available = (statvfs_result.f_frsize * statvfs_result.f_bavail)
    except OSError:
        pass
    return (size_total, size_available)
