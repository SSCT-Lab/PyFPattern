def docker_rm(args, container_id):
    '\n    :type args: EnvironmentConfig\n    :type container_id: str\n    '
    docker_command(args, ['rm', '-f', container_id], capture=True)