

def get_proposed(self):
    'Compare playbook values against existing states and create a list\n        of proposed commands.\n        Return a list of raw cli command strings.\n        '
    ref = self._ref
    proposed = ref['_proposed']
    if (ref['_context'] and ref['_context'][(- 1)].startswith('no')):
        [proposed.append(ctx) for ctx in ref['_context']]
        return proposed
    play_keys = [k for k in ref['commands'] if ('playval' in ref[k])]

    def compare(playval, existing):
        if (ref['_state'] in self.present_states):
            if (existing is None):
                return False
            elif (playval == existing):
                return True
            elif (isinstance(existing, dict) and (playval in existing.values())):
                return True
        if (ref['_state'] in self.absent_states):
            if (isinstance(existing, dict) and all(((x is None) for x in existing.values()))):
                existing = None
            if ((existing is None) or (playval not in existing.values())):
                return True
        return False
    for k in play_keys:
        playval = ref[k]['playval']
        playval_copy = deepcopy(playval)
        existing = ref[k].get('existing', ref[k]['default'])
        multiple = ('multiple' in ref[k].keys())
        if (isinstance(existing, dict) and multiple):
            item_found = False
            for (ekey, evalue) in existing.items():
                if isinstance(evalue, dict):
                    evalue = dict(((k, v) for (k, v) in evalue.items() if (v != 'None')))
                for (pkey, pvalue) in playval.items():
                    if compare(pvalue, evalue):
                        if playval_copy.get(pkey):
                            del playval_copy[pkey]
            if (not playval_copy):
                continue
        else:
            for (pkey, pval) in playval.items():
                if compare(pval, existing):
                    if playval_copy.get(pkey):
                        del playval_copy[pkey]
            if (not playval_copy):
                continue
        playval = playval_copy
        if isinstance(existing, dict):
            for (dkey, dvalue) in existing.items():
                for pval in playval.values():
                    self.build_cmd_set(pval, dvalue, k)
        else:
            for pval in playval.values():
                self.build_cmd_set(pval, existing, k)
    cmds = sorted(set(proposed), key=(lambda x: proposed.index(x)))
    return cmds
