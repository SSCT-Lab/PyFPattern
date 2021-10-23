@property
def group_extractors(self):
    return {
        'sites': self.extract_site,
        'tenants': self.extract_tenant,
        'racks': self.extract_rack,
        'tags': self.extract_tags,
        'disk': self.extract_disk,
        'memory': self.extract_memory,
        'vcpus': self.extract_vcpus,
        'device_roles': self.extract_device_role,
        'device_types': self.extract_device_type,
        'manufacturers': self.extract_manufacturer,
    }