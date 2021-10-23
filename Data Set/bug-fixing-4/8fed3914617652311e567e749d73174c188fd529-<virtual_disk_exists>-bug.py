def virtual_disk_exists(self):
    response = self.get_virtual_disk_on_device()
    if response:
        return True
    return False