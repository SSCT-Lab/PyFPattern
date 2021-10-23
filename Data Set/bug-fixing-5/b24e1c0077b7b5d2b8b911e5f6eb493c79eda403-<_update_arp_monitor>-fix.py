def _update_arp_monitor(self, key, want, have):
    commands = []
    want_arp_target = []
    have_arp_target = []
    want_arp_monitor = (want.get(key) or {
        
    })
    have_arp_monitor = (have.get(key) or {
        
    })
    if (want_arp_monitor and ('target' in want_arp_monitor)):
        want_arp_target = want_arp_monitor['target']
    if (have_arp_monitor and ('target' in have_arp_monitor)):
        have_arp_target = have_arp_monitor['target']
    if (('interval' in have_arp_monitor) and (not want_arp_monitor)):
        commands.append(self._compute_command(key=(have['name'] + ' arp-monitor'), attrib='interval', remove=True))
    if ('target' in have_arp_monitor):
        target_diff = list_diff_have_only(want_arp_target, have_arp_target)
        if target_diff:
            for target in target_diff:
                commands.append(self._compute_command(key=(have['name'] + ' arp-monitor'), attrib='target', value=target, remove=True))
    return commands