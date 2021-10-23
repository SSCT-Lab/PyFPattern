def docker_rm(args, container_id):
    '\n    :type args: EnvironmentConfig\n    :type container_id: str\n    '
    try:
        docker_command(args, ['rm', '-f', container_id], capture=True)
    except SubprocessError as ex:
        if ('no such container' in ex.stderr):
            pass
        else:
            raise ex