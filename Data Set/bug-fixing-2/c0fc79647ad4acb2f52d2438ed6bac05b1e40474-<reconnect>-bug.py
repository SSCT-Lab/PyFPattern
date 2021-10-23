

def reconnect(self):
    'Attempts to reconnect to a device\n\n        The existing token from a ManagementRoot can become invalid if you,\n        for example, upgrade the device (such as is done in the *_software\n        module.\n\n        This method can be used to reconnect to a remote device without\n        having to re-instantiate the ArgumentSpec and AnsibleF5Client classes\n        it will use the same values that were initially provided to those\n        classes\n\n        :return:\n        :raises iControlUnexpectedHTTPError\n        '
    self.client.api = self._get_mgmt_root(self.f5_product_name, **self._connect_params)
