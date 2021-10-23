def run_formatter(cmd, file_list, prompt_on_changes=True):
    if (not file_list):
        return False
    has_errors = False
    status = subprocess.Popen((cmd + file_list)).wait()
    has_errors = (status != 0)
    if has_errors:
        return True
    output = subprocess.check_output((['git', 'diff'] + file_list))
    if output:
        echo('[sentry.lint] applied changes from autoformatting')
        for line in output.splitlines():
            if line.startswith('-'):
                secho(line, fg='red')
            elif line.startswith('+'):
                secho(line, fg='green')
            else:
                echo(line)
        if prompt_on_changes:
            with open('/dev/tty') as fp:
                secho('Stage this patch and continue? [Y/n] ', bold=True)
                if (fp.readline().strip().lower() != 'y'):
                    echo('[sentry.lint] Aborted! Changes have been applied but not staged.', err=True)
                    if (not os.environ.get('SENTRY_SKIP_FORCE_PATCH')):
                        sys.exit(1)
                else:
                    status = subprocess.Popen((['git', 'update-index', '--add'] + file_list)).wait()
        has_errors = (status != 0)
    return has_errors