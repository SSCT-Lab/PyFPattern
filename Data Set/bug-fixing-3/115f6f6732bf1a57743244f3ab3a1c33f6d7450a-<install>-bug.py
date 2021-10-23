def install(module, tserver):
    changed = False
    params = module.params
    name = params['name']
    values = params['values']
    chart = module.params['chart']
    namespace = module.params['namespace']
    chartb = chartbuilder.ChartBuilder(chart)
    try:
        tserver.install_release(chartb.get_helm_chart(), namespace, dry_run=False, name=name, values=values)
        changed = True
    except grpc._channel._Rendezvous as exc:
        if ('already exists' not in str(exc)):
            raise exc
    return dict(changed=changed)