def ansible_facts(module, gather_subset):
    facts = {
        
    }
    facts['gather_subset'] = list(gather_subset)
    facts.update(Facts(module).populate())
    for subset in gather_subset:
        facts.update(FACT_SUBSETS[subset](module).populate())
    return facts