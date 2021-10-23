def __init__(self):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--project')
    parser.add_argument('--domain')
    options = parser.parse_args()
    try:
        self.cs = CloudStack(**read_config())
    except CloudStackException as e:
        print('Error: Could not connect to CloudStack API', file=sys.stderr)
        sys.exit(1)
    domain_id = None
    if options.domain:
        domain_id = self.get_domain_id(options.domain)
    project_id = None
    if options.project:
        project_id = self.get_project_id(options.project, domain_id)
    if options.host:
        data = self.get_host(options.host, project_id, domain_id)
        print(json.dumps(data, indent=2))
    elif options.list:
        data = self.get_list(project_id, domain_id)
        print(json.dumps(data, indent=2))
    else:
        print('usage: --list | --host <hostname> [--project <project>] [--domain <domain_path>]', file=sys.stderr)
        sys.exit(1)