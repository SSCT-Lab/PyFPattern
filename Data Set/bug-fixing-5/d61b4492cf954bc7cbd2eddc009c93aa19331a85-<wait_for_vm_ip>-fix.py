def wait_for_vm_ip(content, vm, timeout=300):
    facts = dict()
    interval = 15
    while (timeout > 0):
        _facts = gather_vm_facts(content, vm)
        if (_facts['ipv4'] or _facts['ipv6']):
            facts = _facts
            break
        time.sleep(interval)
        timeout -= interval
    return facts