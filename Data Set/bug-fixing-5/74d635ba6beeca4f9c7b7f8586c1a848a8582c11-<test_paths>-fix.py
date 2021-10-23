def test_paths(self, args, paths):
    '\n        :type args: SanityConfig\n        :type paths: list[str]\n        :rtype: list[SanityMessage]\n        '
    cmd = ([('python%s' % args.python_version), 'test/sanity/yamllint/yamllinter.py'] + paths)
    try:
        (stdout, stderr) = run_command(args, cmd, capture=True)
        status = 0
    except SubprocessError as ex:
        stdout = ex.stdout
        stderr = ex.stderr
        status = ex.status
    if stderr:
        raise SubprocessError(cmd=cmd, status=status, stderr=stderr, stdout=stdout)
    if args.explain:
        return []
    results = json.loads(stdout)['messages']
    results = [SanityMessage(code=r['code'], message=r['message'], path=r['path'], line=int(r['line']), column=int(r['column']), level=r['level']) for r in results]
    return results