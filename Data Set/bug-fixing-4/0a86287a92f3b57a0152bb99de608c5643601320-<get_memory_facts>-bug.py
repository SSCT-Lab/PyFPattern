def get_memory_facts(self, collected_facts=None):
    memory_facts = {
        
    }
    collected_facts = (collected_facts or {
        
    })
    pagesize = 4096
    (rc, out, err) = self.module.run_command('/usr/bin/vmstat | tail -1', use_unsafe_shell=True)
    data = int(re.sub(' +', ' ', out).split(' ')[5].strip())
    memory_facts['memfree_mb'] = (((pagesize * data) // 1024) // 1024)
    if (collected_facts.get('ansible_architecture') == '9000/800'):
        try:
            (rc, out, err) = self.module.run_command('grep Physical /var/adm/syslog/syslog.log')
            data = re.search('.*Physical: ([0-9]*) Kbytes.*', out).groups()[0].strip()
            memory_facts['memtotal_mb'] = (int(data) // 1024)
        except AttributeError:
            if os.access('/dev/kmem', os.R_OK):
                (rc, out, err) = self.module.run_command("echo 'phys_mem_pages/D' | adb -k /stand/vmunix /dev/kmem | tail -1 | awk '{print $2}'", use_unsafe_shell=True)
                if (not err):
                    data = out
                    memory_facts['memtotal_mb'] = (int(data) / 256)
    else:
        (rc, out, err) = self.module.run_command('/usr/contrib/bin/machinfo | grep Memory', use_unsafe_shell=True)
        data = re.search('Memory[\\ :=]*([0-9]*).*MB.*', out).groups()[0].strip()
        memory_facts['memtotal_mb'] = int(data)
    (rc, out, err) = self.module.run_command('/usr/sbin/swapinfo -m -d -f -q')
    memory_facts['swaptotal_mb'] = int(out.strip())
    (rc, out, err) = self.module.run_command("/usr/sbin/swapinfo -m -d -f | egrep '^dev|^fs'", use_unsafe_shell=True)
    swap = 0
    for line in out.strip().splitlines():
        swap += int(re.sub(' +', ' ', line).split(' ')[3].strip())
    memory_facts['swapfree_mb'] = swap
    return memory_facts