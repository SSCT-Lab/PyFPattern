def get_route53_records(self):
    ' Get and store the map of resource records to domain names that\n        point to them. '
    r53_conn = route53.Route53Connection()
    all_zones = r53_conn.get_zones()
    route53_zones = [zone for zone in all_zones if (zone.name[:(- 1)] not in self.route53_excluded_zones)]
    self.route53_records = {
        
    }
    for zone in route53_zones:
        rrsets = r53_conn.get_all_rrsets(zone.id)
        for record_set in rrsets:
            record_name = record_set.name
            if record_name.endswith('.'):
                record_name = record_name[:(- 1)]
            for resource in record_set.resource_records:
                self.route53_records.setdefault(resource, set())
                self.route53_records[resource].add(record_name)