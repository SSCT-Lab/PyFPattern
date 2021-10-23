def gather_drs_rule_facts(self):
    '\n        Function to gather DRS rule facts about given cluster\n        Returns: Dictinary of clusters with DRS facts\n\n        '
    cluster_rule_facts = dict()
    for cluster_obj in self.cluster_obj_list:
        cluster_rule_facts[cluster_obj.name] = []
        for drs_rule in cluster_obj.configuration.rule:
            if isinstance(drs_rule, vim.cluster.VmHostRuleInfo):
                cluster_rule_facts[cluster_obj.name].append(self.normalize_vm_host_rule_spec(rule_obj=drs_rule))
            else:
                cluster_rule_facts[cluster_obj.name].append(self.normalize_vm_vm_rule_spec(rule_obj=drs_rule))
    return cluster_rule_facts