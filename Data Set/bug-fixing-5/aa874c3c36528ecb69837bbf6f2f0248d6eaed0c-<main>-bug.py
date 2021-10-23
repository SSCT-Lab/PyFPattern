def main():
    argument_spec = InfluxDb.influxdb_argument_spec()
    argument_spec.update(query=dict(type='str', required=True), database_name=dict(required=True, type='str'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    influx = AnsibleInfluxDBRead(module)
    query = module.params.get('query')
    results = influx.read_by_query(query)
    module.exit_json(changed=True, results=results)