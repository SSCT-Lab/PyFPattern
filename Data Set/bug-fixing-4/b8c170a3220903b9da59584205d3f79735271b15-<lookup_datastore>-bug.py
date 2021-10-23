def lookup_datastore(self):
    ' Get datastore(s) per ESXi host or vCenter server '
    datastores = self.cache.get_all_objs(self.content, [vim.Datastore], confine_to_datacenter=True)
    return datastores