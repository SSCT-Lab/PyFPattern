def install(module, tserver):
    changed = False
    params = module.params
    name = params['name']
    values = params['values']
    chart = module.params['chart']
    namespace = module.params['namespace']
    chartb = chartbuilder.ChartBuilder(chart)
    r_matches = (x for x in tserver.list_releases() if ((x.name == name) and (x.namespace == namespace)))
    installed_release = next(r_matches, None)
    if installed_release:
        if (installed_release.chart.metadata.version != chart['version']):
            tserver.update_release(chartb.get_helm_chart(), False, namespace, name=name, values=values)
            changed = True
    else:
        tserver.install_release(chartb.get_helm_chart(), namespace, dry_run=False, name=name, values=values)
        changed = True
    return dict(changed=changed)