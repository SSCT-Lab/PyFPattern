

def main():
    'Main entry point.'
    with open('shippable.yml', 'rb') as yaml_file:
        yaml = yaml_file.read().decode('utf-8').splitlines()
    defined_matrix = [match.group(1) for match in [re.search('^ *- env: T=(.*)$', line) for line in yaml] if (match and (match.group(1) != 'none'))]
    if (not defined_matrix):
        fail('No matrix entries found in the "shippable.yml" file.', 'Did you modify the "shippable.yml" file?')
    run_id = os.environ['SHIPPABLE_BUILD_ID']
    sleep = 1
    jobs = []
    for attempts_remaining in range(4, (- 1), (- 1)):
        try:
            jobs = json.loads(urlopen(('https://api.shippable.com/jobs?runIds=%s' % run_id)).read())
            if (not isinstance(jobs, list)):
                raise Exception(('Shippable run %s data is not a list.' % run_id))
            break
        except Exception as ex:
            if (not attempts_remaining):
                fail(('Unable to retrieve Shippable run %s matrix.' % run_id), str(ex))
            sys.stderr.write(('Unable to retrieve Shippable run %s matrix: %s\n' % (run_id, ex)))
            sys.stderr.write(('Trying again in %d seconds...\n' % sleep))
            time.sleep(sleep)
            sleep *= 2
    if (len(jobs) != len(defined_matrix)):
        if (len(jobs) == 1):
            hint = '\n\nMake sure you do not use the "Rebuild with SSH" option.'
        else:
            hint = ''
        fail(('Shippable run %s has %d jobs instead of the expected %d jobs.' % (run_id, len(jobs), len(defined_matrix))), ('Try re-running the entire matrix.%s' % hint))
    actual_matrix = dict(((job.get('jobNumber'), dict((tuple(line.split('=', 1)) for line in job.get('env', []))).get('T', '')) for job in jobs))
    errors = [(job_number, test, actual_matrix.get(job_number)) for (job_number, test) in enumerate(defined_matrix, 1) if (actual_matrix.get(job_number) != test)]
    if len(errors):
        error_summary = '\n'.join((('Job %s expected "%s" but found "%s" instead.' % (job_number, expected, actual)) for (job_number, expected, actual) in errors))
        fail(('Shippable run %s has a job matrix mismatch.' % run_id), ('Try re-running the entire matrix.\n\n%s' % error_summary))
