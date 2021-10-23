def get_processor_facts(self):
    processor = []
    for i in range(int(self.sysctl['hw.ncpu'])):
        processor.append(self.sysctl['hw.model'])
    self.facts['processor'] = processor
    self.facts['processor_count'] = self.sysctl['hw.ncpu']
    self.facts['processor_cores'] = self.sysctl['hw.ncpu']