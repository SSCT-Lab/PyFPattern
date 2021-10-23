def get_service_offering_id(self):
    service_offering = self.module.params.get('service_offering')
    if (not service_offering):
        return None
    args = {
        'issystem': True,
    }
    service_offerings = self.cs.listServiceOfferings(**args)
    if service_offerings:
        for s in service_offerings['serviceoffering']:
            if (service_offering in [s['name'], s['id']]):
                return s['id']
    self.module.fail_json(msg=("Service offering '%s' not found" % service_offering))