@property
def group_extractors(self):
    return {
        'sites': self.extract_site,
        'tenants': self.extract_tenant,
        'racks': self.extract_rack,
        'tags': self.extract_tags,
        'device_roles': self.extract_device_role,
        'device_types': self.extract_device_type,
        'manufacturers': self.extract_manufacturer,
    }