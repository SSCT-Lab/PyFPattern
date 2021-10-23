

def get_network_legacy_facts(self, fact_legacy_obj_map, legacy_facts_type=None):
    if (not legacy_facts_type):
        legacy_facts_type = self._gather_subset
    runable_subsets = self.gen_runable(legacy_facts_type, frozenset(fact_legacy_obj_map.keys()))
    runable_subsets.add('default')
    if runable_subsets:
        facts = dict()
        facts['ansible_net_gather_subset'] = list(runable_subsets)
        instances = list()
        for key in runable_subsets:
            instances.append(fact_legacy_obj_map[key](self._module))
        for inst in instances:
            inst.populate()
            facts.update(inst.facts)
            self._warnings.extend(inst.warnings)
        for (key, value) in iteritems(facts):
            key = ('ansible_net_%s' % key)
            self.ansible_facts[key] = value
