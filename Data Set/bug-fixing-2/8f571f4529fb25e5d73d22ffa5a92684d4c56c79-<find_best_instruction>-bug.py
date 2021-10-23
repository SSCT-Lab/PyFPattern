

def find_best_instruction(self, frame, meta=None):
    'Finds the best instruction for a given frame.'
    if (not self.images):
        return parse_addr(frame['instruction_addr'])
    return self.symsynd_symbolizer.find_best_instruction(frame['instruction_addr'], cpu_name=self.cpu_name, meta=meta)
