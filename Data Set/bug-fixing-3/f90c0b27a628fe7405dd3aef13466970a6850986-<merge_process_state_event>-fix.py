def merge_process_state_event(data, state, cfi=None):
    data['platform'] = 'native'
    data['level'] = ('fatal' if state.crashed else 'info')
    if state.timestamp:
        data['timestamp'] = float(state.timestamp)
    info = state.system_info
    context = data.setdefault('contexts', {
        
    })
    os = context.setdefault('os', {
        
    })
    device = context.setdefault('device', {
        
    })
    os['type'] = 'os'
    os['name'] = MINIDUMP_OS_TYPES.get(info.os_name, info.os_name)
    os['version'] = info.os_version
    os['build'] = info.os_build
    device['arch'] = arch_from_breakpad(info.cpu_family)
    data['threads'] = [{
        'id': thread.thread_id,
        'crashed': False,
        'stacktrace': {
            'frames': frames_from_minidump_thread(thread),
            'registers': (thread.get_frame(0).registers if thread.frame_count else None),
        },
    } for thread in state.threads()]
    crashed_thread = data['threads'][state.requesting_thread]
    crashed_thread['crashed'] = True
    exc_value = (('Assertion Error: %s' % state.assertion) if state.assertion else ('Fatal Error: %s' % state.crash_reason))
    data['exception'] = {
        'value': exc_value,
        'thread_id': crashed_thread['id'],
        'type': state.crash_reason,
        'stacktrace': crashed_thread.pop('stacktrace'),
        'mechanism': {
            'type': 'minidump',
            'handled': False,
        },
    }
    images = [{
        'type': 'symbolic',
        'id': id_from_breakpad(module.id),
        'image_addr': ('0x%x' % module.addr),
        'image_size': module.size,
        'name': module.name,
    } for module in state.modules() if is_valid_module_id(module.id)]
    data.setdefault('debug_meta', {
        
    })['images'] = images