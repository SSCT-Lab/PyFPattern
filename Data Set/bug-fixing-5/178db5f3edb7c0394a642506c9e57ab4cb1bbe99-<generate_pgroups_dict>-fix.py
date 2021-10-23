def generate_pgroups_dict(array):
    pgroups_facts = {
        
    }
    pgroups = array.list_pgroups()
    for pgroup in range(0, len(pgroups)):
        protgroup = pgroups[pgroup]['name']
        pgroups_facts[protgroup] = {
            'hgroups': pgroups[pgroup]['hgroups'],
            'hosts': pgroups[pgroup]['hosts'],
            'source': pgroups[pgroup]['source'],
            'targets': pgroups[pgroup]['targets'],
            'volumes': pgroups[pgroup]['volumes'],
        }
        prot_sched = array.get_pgroup(protgroup, schedule=True)
        prot_reten = array.get_pgroup(protgroup, retention=True)
        if (prot_sched['snap_enabled'] or prot_sched['replicate_enabled']):
            pgroups_facts[protgroup]['snap_freqyency'] = prot_sched['snap_frequency']
            pgroups_facts[protgroup]['replicate_freqyency'] = prot_sched['replicate_frequency']
            pgroups_facts[protgroup]['snap_enabled'] = prot_sched['snap_enabled']
            pgroups_facts[protgroup]['replicate_enabled'] = prot_sched['replicate_enabled']
            pgroups_facts[protgroup]['snap_at'] = prot_sched['snap_at']
            pgroups_facts[protgroup]['replicate_at'] = prot_sched['replicate_at']
            pgroups_facts[protgroup]['replicate_blackout'] = prot_sched['replicate_blackout']
            pgroups_facts[protgroup]['per_day'] = prot_reten['per_day']
            pgroups_facts[protgroup]['target_per_day'] = prot_reten['target_per_day']
            pgroups_facts[protgroup]['target_days'] = prot_reten['target_days']
            pgroups_facts[protgroup]['days'] = prot_reten['days']
            pgroups_facts[protgroup]['all_for'] = prot_reten['all_for']
            pgroups_facts[protgroup]['target_all_for'] = prot_reten['target_all_for']
        if (':' in protgroup):
            snap_transfers = array.get_pgroup(protgroup, snap=True, transfer=True)
            pgroups_facts[protgroup]['snaps'] = {
                
            }
            for snap_transfer in range(0, len(snap_transfers)):
                snap = snap_transfers[snap_transfer]['name']
                pgroups_facts[protgroup]['snaps'][snap] = {
                    'created': snap_transfers[snap_transfer]['created'],
                    'started': snap_transfers[snap_transfer]['started'],
                    'completed': snap_transfers[snap_transfer]['completed'],
                    'physical_bytes_written': snap_transfers[snap_transfer]['physical_bytes_written'],
                    'data_transferred': snap_transfers[snap_transfer]['data_transferred'],
                    'progress': snap_transfers[snap_transfer]['progress'],
                }
    return pgroups_facts