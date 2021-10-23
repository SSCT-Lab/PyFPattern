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
    return pgroups_facts