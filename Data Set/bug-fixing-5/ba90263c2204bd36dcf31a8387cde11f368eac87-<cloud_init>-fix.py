def cloud_init(args, targets):
    '\n    :type args: IntegrationConfig\n    :type targets: tuple[IntegrationTarget]\n    '
    if (args.metadata.cloud_config is not None):
        return
    args.metadata.cloud_config = {
        
    }
    results = {
        
    }
    for provider in get_cloud_providers(args, targets):
        args.metadata.cloud_config[provider.platform] = {
            
        }
        start_time = time.time()
        provider.setup()
        end_time = time.time()
        results[provider.platform] = dict(platform=provider.platform, setup_seconds=int((end_time - start_time)), targets=[target.name for target in targets])
    if ((not args.explain) and results):
        results_path = ('test/results/data/%s-%s.json' % (args.command, re.sub('[^0-9]', '-', str(datetime.datetime.utcnow().replace(microsecond=0)))))
        data = dict(clouds=results)
        make_dirs(os.path.dirname(results_path))
        with open(results_path, 'w') as results_fd:
            results_fd.write(json.dumps(data, sort_keys=True, indent=4))