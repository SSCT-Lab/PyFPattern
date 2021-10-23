def get_processor_facts(self):
    processor = []
    dmesg_boot = get_file_content(OpenBSDHardware.DMESG_BOOT)
    if (not dmesg_boot):
        (rc, dmesg_boot, err) = self.module.run_command('/sbin/dmesg')
    i = 0
    for line in dmesg_boot.splitlines():
        if (line.split(' ', 1)[0] == ('cpu%i:' % i)):
            processor.append(line.split(' ', 1)[1])
            i = (i + 1)
    processor_count = i
    self.facts['processor'] = processor
    self.facts['processor_count'] = processor_count
    self.facts['processor_cores'] = 'NA'