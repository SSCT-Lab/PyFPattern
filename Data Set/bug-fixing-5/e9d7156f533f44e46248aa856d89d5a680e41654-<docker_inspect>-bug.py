def docker_inspect(args, container_id):
    '\n    :type args: EnvironmentConfig\n    :type container_id: str\n    :rtype: list[dict]\n    '
    if args.explain:
        return []
    try:
        stdout = docker_command(args, ['inspect', container_id], capture=True)[0]
        return json.loads(stdout)
    except SubprocessError as ex:
        try:
            return json.loads(ex.stdout)
        except Exception:
            raise ex