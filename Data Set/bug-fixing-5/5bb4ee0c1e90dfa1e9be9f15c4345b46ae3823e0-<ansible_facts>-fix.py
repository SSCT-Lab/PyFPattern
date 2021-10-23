def ansible_facts(module, gather_subset):
    facts = {
        
    }
    facts['gather_subset'] = list(gather_subset)
    facts.update(Facts(module).populate())
    for subset in gather_subset:
        facts.update(FACT_SUBSETS[subset](module, load_on_init=False, cached_facts=facts).populate())
    return facts