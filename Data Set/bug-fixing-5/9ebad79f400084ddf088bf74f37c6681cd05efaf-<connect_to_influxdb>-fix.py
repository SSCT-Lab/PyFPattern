def connect_to_influxdb(self):
    args = dict(host=self.hostname, port=self.port, username=self.username, password=self.password, database=self.database_name, ssl=self.params['ssl'], verify_ssl=self.params['validate_certs'], timeout=self.params['timeout'], use_udp=self.params['use_udp'], udp_port=self.params['udp_port'], proxies=self.params['proxies'])
    influxdb_api_version = tuple(influxdb_version.split('.'))
    if (influxdb_api_version >= ('4', '1', '0')):
        args.update(retries=self.params['retries'])
    return InfluxDBClient(**args)