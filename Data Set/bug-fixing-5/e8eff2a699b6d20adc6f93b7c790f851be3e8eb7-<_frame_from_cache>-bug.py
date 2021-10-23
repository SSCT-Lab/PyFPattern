def _frame_from_cache(self, entry):
    (debug_id, offset, trust) = entry[:3]
    module = self.modules.get_object(debug_id)
    addr = ((module.addr + offset) if module else offset)
    return (module, {
        'instruction_addr': ('0x%x' % addr),
        'function': '<unknown>',
        'module': (module.name if module else None),
        'trust': trust,
    })