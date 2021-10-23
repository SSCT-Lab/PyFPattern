def _change_value(self, key, value):
    if (key in ['region', 'pool', 'datacenter']):
        return (key, fq_name(self.partition, value))
    if (key == 'isp'):
        return (key, fq_name('Common', value))
    if (key == 'continent'):
        return (key, self.continents.get(value, value))
    if (key == 'country'):
        return (key, self.countries.get(value, value))
    if (key == 'geo_isp'):
        return ('geoip-isp', value)
    return (key, value)