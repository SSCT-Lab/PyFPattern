def _parse_properties(module):
    p = module.params['properties']
    props = dict(cpu_arch=(p.get('cpu_arch') if p.get('cpu_arch') else 'x86_64'), cpus=(p.get('cpus') if p.get('cpus') else 1), memory_mb=(p.get('ram') if p.get('ram') else 1), local_gb=(p.get('disk_size') if p.get('disk_size') else 1), capabilities=(p.get('capabilities') if p.get('capabilities') else ''), root_device=(p.get('root_device') if p.get('root_device') else ''))
    return props