

def payload(self, aci_class, class_config, child_configs=None):
    "\n        This method is used to dynamically build the proposed configuration dictionary from the config related parameters\n        passed into the module. All values that were not passed values from the playbook task will be removed so as to not\n        inadvertently change configurations.\n\n        :param aci_class: Type str\n                          This is the root dictionary key for the MO's configuration body, or the ACI class of the MO.\n        :param class_config: Type dict\n                             This is the configuration of the MO using the dictionary keys expected by the API\n        :param child_configs: Type list\n                              This is a list of child dictionaries associated with the MOs config. The list should only\n                              include child objects that are used to associate two MOs together. Children that represent\n                              MOs should have their own module.\n        "
    proposed = dict(((k, str(v)) for (k, v) in class_config.items() if (v is not None)))
    self.result['proposed'] = {
        aci_class: {
            'attributes': proposed,
        },
    }
    if child_configs:
        children = []
        for child in child_configs:
            has_value = False
            for root_key in child.keys():
                for (final_keys, values) in child[root_key]['attributes'].items():
                    if (values is None):
                        child[root_key]['attributes'].pop(final_keys)
                    else:
                        child[root_key]['attributes'][final_keys] = str(values)
                        has_value = True
            if has_value:
                children.append(child)
        if children:
            self.result['proposed'][aci_class].update(dict(children=children))
