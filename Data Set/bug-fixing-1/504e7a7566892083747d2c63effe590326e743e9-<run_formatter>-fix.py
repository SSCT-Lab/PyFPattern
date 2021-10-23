

def run_formatter(cmd, file_list, prompt_on_changes=True):
    if (not file_list):
        return False
    has_errors = False
    status = subprocess.Popen((cmd + file_list)).wait()
    has_errors = (status != 0)
    if has_errors:
        return True
    output = subprocess.check_output((['git', 'diff', '--color'] + file_list))
    if output:
        print('[sentry.lint] applied changes from autoformatting')
        print(output)
        if prompt_on_changes:
            with open('/dev/tty') as fp:
                print((('\x1b[1m' + 'Stage this patch and continue? [Y/n] ') + '\x1b[0m'))
                if (fp.readline().strip() not in ('Y', 'y', '')):
                    print('[sentry.lint] Unstaged changes have not been staged.', file=sys.stderr)
                    if (not os.environ.get('SENTRY_SKIP_FORCE_PATCH')):
                        print('[sentry.lint] Aborted!', file=sys.stderr)
                        sys.exit(1)
                else:
                    status = subprocess.Popen((['git', 'update-index', '--add'] + file_list)).wait()
        has_errors = (status != 0)
    return has_errors
