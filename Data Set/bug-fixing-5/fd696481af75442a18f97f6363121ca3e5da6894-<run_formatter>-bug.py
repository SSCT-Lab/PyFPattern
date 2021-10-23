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
        print('[sentry.lint] applied changes from autoformatting')
        for line in output.splitlines():
            if line.startswith('-'):
                print((('\x1b[41m' + line) + '\x1b[0m'))
            elif line.startswith('+'):
                print((('\x1b[42m' + line) + '\x1b[0m'))
            else:
                print(line)
        if prompt_on_changes:
            with open('/dev/tty') as fp:
                print((('\x1b[1m' + 'Stage this patch and continue? [Y/n] ') + '\x1b[0m'))
                if (fp.readline().strip().lower() != 'y'):
                    print('[sentry.lint] Aborted! Changes have been applied but not staged.', file=sys.stderr)
                    if (not os.environ.get('SENTRY_SKIP_FORCE_PATCH')):
                        sys.exit(1)
                else:
                    status = subprocess.Popen((['git', 'update-index', '--add'] + file_list)).wait()
        has_errors = (status != 0)
    return has_errors