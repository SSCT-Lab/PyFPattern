

def walk_integration_targets():
    '\n    :rtype: collections.Iterable[IntegrationTarget]\n    '
    path = 'test/integration/targets'
    modules = frozenset((t.module for t in walk_module_targets()))
    paths = sorted((os.path.join(path, p) for p in os.listdir(path)))
    prefixes = load_integration_prefixes()
    for path in paths:
        (yield IntegrationTarget(path, modules, prefixes))
