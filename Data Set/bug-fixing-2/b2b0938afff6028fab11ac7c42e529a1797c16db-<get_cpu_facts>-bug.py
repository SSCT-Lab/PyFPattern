

def get_cpu_facts(self):
    cpu_facts = {
        
    }
    cpu_facts['processor'] = []
    (rc, out, err) = self.module.run_command('/usr/sbin/lsdev -Cc processor')
    if out:
        i = 0
        for line in out.splitlines():
            if ('Available' in line):
                if (i == 0):
                    data = line.split(' ')
                    cpudev = data[0]
                i += 1
        cpu_facts['processor_count'] = int(i)
        (rc, out, err) = self.module.run_command((('/usr/sbin/lsattr -El ' + cpudev) + ' -a type'))
        data = out.split(' ')
        cpu_facts['processor'] = data[1]
        (rc, out, err) = self.module.run_command((('/usr/sbin/lsattr -El ' + cpudev) + ' -a smt_threads'))
        data = out.split(' ')
        cpu_facts['processor_cores'] = int(data[1])
    return cpu_facts
