

def get_configured_disk_size(self, expected_disk_spec):
    if [x for x in expected_disk_spec.keys() if (x.startswith('size_') or (x == 'size'))]:
        if ('size' in expected_disk_spec):
            expected = ''.join((c for c in expected_disk_spec['size'] if c.isdigit()))
            unit = expected_disk_spec['size'].replace(expected, '').lower()
            expected = int(expected)
        else:
            param = [x for x in expected_disk_spec.keys() if x.startswith('size_')][0]
            unit = param.split('_')[(- 1)].lower()
            expected = [x[1] for x in expected_disk_spec.items() if x[0].startswith('size_')][0]
            expected = int(expected)
        if (unit == 'tb'):
            return (((expected * 1024) * 1024) * 1024)
        elif (unit == 'gb'):
            return ((expected * 1024) * 1024)
        elif (unit == 'mb'):
            return (expected * 1024)
        elif (unit == 'kb'):
            return expected
        self.module.fail_json(msg=('%s is not a supported unit for disk size. Supported units are kb, mb, gb or tb' % unit))
    self.module.fail_json(msg='No size, size_kb, size_mb, size_gb or size_tb attribute found into disk configuration')
