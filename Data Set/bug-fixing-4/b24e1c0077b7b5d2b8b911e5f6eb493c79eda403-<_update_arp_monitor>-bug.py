def _update_arp_monitor(self, key, want, have):
    commands = []
    want_arp_target = []
    have_arp_target = []
    want_arp_monitor = (want.get(key) or {
        
    })
    have_arp_monitor = (have.get(key) or {
        
    })
    del_cmd = ('delete interface bonding ' + have['name'])
    if (want_arp_monitor and ('target' in want_arp_monitor)):
        want_arp_target = want_arp_monitor['target']
    if (have_arp_monitor and ('target' in have_arp_monitor)):
        have_arp_target = have_arp_monitor['target']
    if (('interval' in have_arp_monitor) and (not want_arp_monitor)):
        commands.append((((del_cmd + ' ') + key) + ' interval'))
    if ('target' in have_arp_monitor):
        target_diff = list_diff_have_only(want_arp_target, have_arp_target)
        if target_diff:
            for target in target_diff:
                commands.append(((((del_cmd + ' ') + key) + ' target ') + target))
    return commands