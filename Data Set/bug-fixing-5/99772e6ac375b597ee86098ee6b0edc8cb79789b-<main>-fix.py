def main():
    'Main program body.'
    api_key = get_api_key()
    parser = argparse.ArgumentParser(description='Start a new Shippable run.')
    parser.add_argument('project', metavar='account/project', help='Shippable account/project')
    target = parser.add_mutually_exclusive_group()
    target.add_argument('--branch', help='branch name')
    target.add_argument('--run', metavar='ID', help='Shippable run ID')
    parser.add_argument('--key', metavar='KEY', default=api_key, required=(not api_key), help='Shippable API key')
    parser.add_argument('--env', nargs=2, metavar=('KEY', 'VALUE'), action='append', help='environment variable to pass')
    if argcomplete:
        argcomplete.autocomplete(parser)
    args = parser.parse_args()
    headers = dict(Authorization=('apiToken %s' % args.key))
    data = dict(projectFullNames=args.project)
    url = 'https://api.shippable.com/projects'
    response = requests.get(url, data, headers=headers)
    if (response.status_code != 200):
        raise Exception(response.content)
    result = response.json()
    if (len(result) != 1):
        raise Exception(('Received %d items instead of 1 looking for %s in:\n%s' % (len(result), args.project, json.dumps(result, indent=4, sort_keys=True))))
    project_id = response.json()[0]['id']
    data = dict(globalEnv=dict(((kp[0], kp[1]) for kp in (args.env or []))))
    if args.branch:
        data['branchName'] = args.branch
    elif args.run:
        data['runId'] = args.run
    url = ('https://api.shippable.com/projects/%s/newBuild' % project_id)
    response = requests.post(url, json=data, headers=headers)
    if (response.status_code != 200):
        raise Exception(('HTTP %s: %s\n%s' % (response.status_code, response.reason, response.content)))
    print(json.dumps(response.json(), indent=4, sort_keys=True))