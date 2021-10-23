def refresh_lookups(self):
    lookup_processes = (self.refresh_sites_lookup, self.refresh_regions_lookup, self.refresh_tenants_lookup, self.refresh_racks_lookup, self.refresh_device_roles_lookup, self.refresh_platforms_lookup, self.refresh_device_types_lookup, self.refresh_manufacturers_lookup)
    thread_list = []
    for p in lookup_processes:
        t = Thread(target=p)
        thread_list.append(t)
        t.start()
    for thread in thread_list:
        thread.join()