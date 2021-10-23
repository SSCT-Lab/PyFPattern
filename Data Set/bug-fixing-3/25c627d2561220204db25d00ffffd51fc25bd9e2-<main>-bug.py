def main():
    'Main program body.'
    api_key = get_api_key()
    parser = argparse.ArgumentParser(description='Download results from a Shippable run.')
    parser.add_argument('run_id', metavar='RUN', help='shippable run id, run url or run name formatted as: account/project/run_number')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='show what is being downloaded')
    parser.add_argument('-t', '--test', dest='test', action='store_true', help='show what would be downloaded without downloading')
    parser.add_argument('--key', dest='api_key', default=api_key, required=(api_key is None), help='api key for accessing Shippable')
    parser.add_argument('--console-logs', action='store_true', help='download console logs')
    parser.add_argument('--test-results', action='store_true', help='download test results')
    parser.add_argument('--coverage-results', action='store_true', help='download code coverage results')
    parser.add_argument('--job-metadata', action='store_true', help='download job metadata')
    parser.add_argument('--run-metadata', action='store_true', help='download run metadata')
    parser.add_argument('--all', action='store_true', help='download everything')
    parser.add_argument('--job-number', metavar='N', action='append', type=int, help='limit downloads to the given job number')
    if argcomplete:
        argcomplete.autocomplete(parser)
    args = parser.parse_args()
    old_runs_prefix = 'https://app.shippable.com/runs/'
    if args.run_id.startswith(old_runs_prefix):
        args.run_id = args.run_id[len(old_runs_prefix):]
    if args.all:
        args.console_logs = True
        args.test_results = True
        args.coverage_results = True
        args.job_metadata = True
        args.run_metadata = True
    selections = (args.console_logs, args.test_results, args.coverage_results, args.job_metadata, args.run_metadata)
    if (not any(selections)):
        parser.error('At least one download option is required.')
    headers = dict(Authorization=('apiToken %s' % args.api_key))
    match = re.search('^https://app.shippable.com/github/(?P<account>[^/]+)/(?P<project>[^/]+)/runs/(?P<run_number>[0-9]+)(?:/summary|(/(?P<job_number>[0-9]+)))?$', args.run_id)
    if (not match):
        match = re.search('^(?P<account>[^/]+)/(?P<project>[^/]+)/(?P<run_number>[0-9]+)$', args.run_id)
    if match:
        account = match.group('account')
        project = match.group('project')
        run_number = int(match.group('run_number'))
        job_number = (int(match.group('job_number')) if match.group('job_number') else None)
        if job_number:
            if args.job_number:
                exit('ERROR: job number found in url and specified with --job-number')
            args.job_number = [job_number]
        url = 'https://api.shippable.com/projects'
        response = requests.get(url, dict(projectFullNames=('%s/%s' % (account, project))), headers=headers)
        if (response.status_code != 200):
            raise Exception(response.content)
        project_id = response.json()[0]['id']
        url = ('https://api.shippable.com/runs?projectIds=%s&runNumbers=%s' % (project_id, run_number))
        response = requests.get(url, headers=headers)
        if (response.status_code != 200):
            raise Exception(response.content)
        run = [run for run in response.json() if (run['runNumber'] == run_number)][0]
        args.run_id = run['id']
    elif re.search('^[a-f0-9]+$', args.run_id):
        url = ('https://api.shippable.com/runs/%s' % args.run_id)
        response = requests.get(url, headers=headers)
        if (response.status_code != 200):
            raise Exception(response.content)
        run = response.json()
        account = run['subscriptionOrgName']
        project = run['projectName']
        run_number = run['runNumber']
    else:
        exit(('ERROR: invalid run: %s' % args.run_id))
    output_dir = ('%s/%s/%s' % (account, project, run_number))
    response = requests.get(('https://api.shippable.com/jobs?runIds=%s' % args.run_id), headers=headers)
    if (response.status_code != 200):
        raise Exception(response.content)
    jobs = sorted(response.json(), key=(lambda job: int(job['jobNumber'])))
    if (not args.test):
        if (not os.path.exists(output_dir)):
            os.makedirs(output_dir)
    if args.run_metadata:
        path = os.path.join(output_dir, 'run.json')
        contents = json.dumps(run, sort_keys=True, indent=4)
        if (args.verbose or args.test):
            print(path)
        if (not args.test):
            with open(path, 'w') as metadata_fd:
                metadata_fd.write(contents)
    for j in jobs:
        job_id = j['id']
        job_number = j['jobNumber']
        if (args.job_number and (job_number not in args.job_number)):
            continue
        if args.job_metadata:
            path = os.path.join(output_dir, ('%s/job.json' % job_number))
            contents = json.dumps(j, sort_keys=True, indent=4)
            if (args.verbose or args.test):
                print(path)
            if (not args.test):
                directory = os.path.dirname(path)
                if (not os.path.exists(directory)):
                    os.makedirs(directory)
                with open(path, 'w') as metadata_fd:
                    metadata_fd.write(contents)
        if args.console_logs:
            path = os.path.join(output_dir, ('%s/console.log' % job_number))
            url = ('https://api.shippable.com/jobs/%s/consoles?download=true' % job_id)
            download(args, headers, path, url, is_json=False)
        if args.test_results:
            path = os.path.join(output_dir, ('%s/test.json' % job_number))
            url = ('https://api.shippable.com/jobs/%s/jobTestReports' % job_id)
            download(args, headers, path, url)
            extract_contents(args, path, os.path.join(output_dir, ('%s/test' % job_number)))
        if args.coverage_results:
            path = os.path.join(output_dir, ('%s/coverage.json' % job_number))
            url = ('https://api.shippable.com/jobs/%s/jobCoverageReports' % job_id)
            download(args, headers, path, url)
            extract_contents(args, path, os.path.join(output_dir, ('%s/coverage' % job_number)))