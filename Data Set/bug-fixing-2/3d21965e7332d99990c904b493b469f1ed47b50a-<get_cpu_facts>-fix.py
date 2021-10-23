

def get_cpu_facts(self, collected_facts=None):
    cpu_facts = {
        
    }
    collected_facts = (collected_facts or {
        
    })
    if (collected_facts.get('ansible_architecture') == '9000/800'):
        (rc, out, err) = self.module.run_command('ioscan -FkCprocessor | wc -l', use_unsafe_shell=True)
        cpu_facts['processor_count'] = int(out.strip())
    elif (collected_facts.get('ansible_architecture') == 'ia64'):
        if (collected_facts.get('ansible_distribution_version') == 'B.11.23'):
            (rc, out, err) = self.module.run_command("/usr/contrib/bin/machinfo | grep 'Number of CPUs'", use_unsafe_shell=True)
            if out:
                cpu_facts['processor_count'] = int(out.strip().split('=')[1])
            (rc, out, err) = self.module.run_command("/usr/contrib/bin/machinfo | grep 'processor family'", use_unsafe_shell=True)
            if out:
                cpu_facts['processor'] = re.search('.*(Intel.*)', out).groups()[0].strip()
            (rc, out, err) = self.module.run_command('ioscan -FkCprocessor | wc -l', use_unsafe_shell=True)
            cpu_facts['processor_cores'] = int(out.strip())
        if (collected_facts.get('ansible_distribution_version') == 'B.11.31'):
            (rc, out, err) = self.module.run_command('/usr/contrib/bin/machinfo | grep core | wc -l', use_unsafe_shell=True)
            if (out.strip() == '0'):
                (rc, out, err) = self.module.run_command('/usr/contrib/bin/machinfo | grep Intel', use_unsafe_shell=True)
                cpu_facts['processor_count'] = int(out.strip().split(' ')[0])
                (rc, out, err) = self.module.run_command('/usr/sbin/psrset | grep LCPU', use_unsafe_shell=True)
                data = re.sub(' +', ' ', out).strip().split(' ')
                if (len(data) == 1):
                    hyperthreading = 'OFF'
                else:
                    hyperthreading = data[1]
                (rc, out, err) = self.module.run_command('/usr/contrib/bin/machinfo | grep logical', use_unsafe_shell=True)
                data = out.strip().split(' ')
                if (hyperthreading == 'ON'):
                    cpu_facts['processor_cores'] = (int(data[0]) / 2)
                elif (len(data) == 1):
                    cpu_facts['processor_cores'] = cpu_facts['processor_count']
                else:
                    cpu_facts['processor_cores'] = int(data[0])
                (rc, out, err) = self.module.run_command("/usr/contrib/bin/machinfo | grep Intel |cut -d' ' -f4-", use_unsafe_shell=True)
                cpu_facts['processor'] = out.strip()
            else:
                (rc, out, err) = self.module.run_command("/usr/contrib/bin/machinfo | egrep 'socket[s]?$' | tail -1", use_unsafe_shell=True)
                cpu_facts['processor_count'] = int(out.strip().split(' ')[0])
                (rc, out, err) = self.module.run_command("/usr/contrib/bin/machinfo | grep -e '[0-9] core' | tail -1", use_unsafe_shell=True)
                cpu_facts['processor_cores'] = int(out.strip().split(' ')[0])
                (rc, out, err) = self.module.run_command('/usr/contrib/bin/machinfo | grep Intel', use_unsafe_shell=True)
                cpu_facts['processor'] = out.strip()
    return cpu_facts
