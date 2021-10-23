

def find_best_instruction(self, processable_frame):
    'Given a frame, stacktrace info and frame index this returns the\n        interpolated instruction address we then use for symbolication later.\n        '
    if (self.arch is None):
        return parse_addr(processable_frame['instruction_addr'])
    crashing_frame = False
    signal = None
    ip_reg = None
    if (processable_frame.idx == 0):
        signal = None
        exc = self.data.get('sentry.interfaces.Exception')
        if (exc is not None):
            mechanism = exc['values'][0].get('mechanism')
            if (mechanism and ('posix_signal' in mechanism) and ('signal' in mechanism['posix_signal'])):
                signal = int(mechanism['posix_signal']['signal'])
        registers = processable_frame.stacktrace_info.stacktrace.get('registers')
        if registers:
            ip_reg_name = arch_get_ip_reg_name(self.arch)
            if ip_reg_name:
                ip_reg = registers.get(ip_reg_name)
        crashing_frame = True
    return find_best_instruction(processable_frame['instruction_addr'], arch=self.arch, crashing_frame=crashing_frame, signal=signal, ip_reg=ip_reg)
