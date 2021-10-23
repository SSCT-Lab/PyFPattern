

def wait_for_vm_ip(content, vm, timeout=300):
    facts = dict()
    interval = 15
    while (timeout > 0):
        facts = gather_vm_facts(content, vm)
        if (facts['ipv4'] or facts['ipv6']):
            break
        time.sleep(interval)
        timeout -= interval
    return facts
