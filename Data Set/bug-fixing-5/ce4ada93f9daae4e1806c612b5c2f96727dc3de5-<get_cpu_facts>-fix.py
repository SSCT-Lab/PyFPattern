def get_cpu_facts(self, collected_facts=None):
    cpu_facts = {
        
    }
    collected_facts = (collected_facts or {
        
    })
    i = 0
    vendor_id_occurrence = 0
    model_name_occurrence = 0
    physid = 0
    coreid = 0
    sockets = {
        
    }
    cores = {
        
    }
    xen = False
    xen_paravirt = False
    try:
        if os.path.exists('/proc/xen'):
            xen = True
        else:
            for line in get_file_lines('/sys/hypervisor/type'):
                if (line.strip() == 'xen'):
                    xen = True
                break
    except IOError:
        pass
    if (not os.access('/proc/cpuinfo', os.R_OK)):
        return cpu_facts
    cpu_facts['processor'] = []
    for line in get_file_lines('/proc/cpuinfo'):
        data = line.split(':', 1)
        key = data[0].strip()
        if xen:
            if (key == 'flags'):
                if ('vme' not in data):
                    xen_paravirt = True
        if (key in ['model name', 'Processor', 'vendor_id', 'cpu', 'Vendor', 'processor']):
            if ('processor' not in cpu_facts):
                cpu_facts['processor'] = []
            cpu_facts['processor'].append(data[1].strip())
            if (key == 'vendor_id'):
                vendor_id_occurrence += 1
            if (key == 'model name'):
                model_name_occurrence += 1
            i += 1
        elif (key == 'physical id'):
            physid = data[1].strip()
            if (physid not in sockets):
                sockets[physid] = 1
        elif (key == 'core id'):
            coreid = data[1].strip()
            if (coreid not in sockets):
                cores[coreid] = 1
        elif (key == 'cpu cores'):
            sockets[physid] = int(data[1].strip())
        elif (key == 'siblings'):
            cores[coreid] = int(data[1].strip())
        elif (key == '# processors'):
            cpu_facts['processor_cores'] = int(data[1].strip())
    if (vendor_id_occurrence > 0):
        if (vendor_id_occurrence == model_name_occurrence):
            i = vendor_id_occurrence
    if (collected_facts.get('ansible_architecture') != 's390x'):
        if xen_paravirt:
            cpu_facts['processor_count'] = i
            cpu_facts['processor_cores'] = i
            cpu_facts['processor_threads_per_core'] = 1
            cpu_facts['processor_vcpus'] = i
        else:
            if sockets:
                cpu_facts['processor_count'] = len(sockets)
            else:
                cpu_facts['processor_count'] = i
            socket_values = list(sockets.values())
            if (socket_values and socket_values[0]):
                cpu_facts['processor_cores'] = socket_values[0]
            else:
                cpu_facts['processor_cores'] = 1
            core_values = list(cores.values())
            if core_values:
                cpu_facts['processor_threads_per_core'] = (core_values[0] // cpu_facts['processor_cores'])
            else:
                cpu_facts['processor_threads_per_core'] = (1 // cpu_facts['processor_cores'])
            cpu_facts['processor_vcpus'] = ((cpu_facts['processor_threads_per_core'] * cpu_facts['processor_count']) * cpu_facts['processor_cores'])
    return cpu_facts