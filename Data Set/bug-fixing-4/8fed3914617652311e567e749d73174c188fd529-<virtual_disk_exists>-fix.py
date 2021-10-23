def virtual_disk_exists(self):
    'Checks if a virtual disk exists for a guest\n\n        The virtual disk names can differ based on the device vCMP is installed on.\n        For instance, on a shuttle-series device with no slots, you will see disks\n        that resemble the following\n\n          guest1.img\n\n        On an 8-blade Viprion with slots though, you will see\n\n          guest1.img/1\n\n        The "/1" in this case is the slot that it is a part of. This method looks\n        for the virtual-disk without the trailing slot.\n\n        Returns:\n            dict\n        '
    response = self.get_virtual_disks_on_device()
    check = '{0}'.format(self.have.virtual_disk)
    for resource in response['items']:
        if resource['name'].startswith(check):
            return True
        else:
            return False