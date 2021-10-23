def build_docker(platform: str, docker_binary: str, registry: str) -> None:
    '\n    Build a container for the given platform\n    :param platform: Platform\n    :param docker_binary: docker binary to use (docker/nvidia-docker)\n    :param registry: Dockerhub registry name\n    :return: Id of the top level image\n    '
    tag = get_docker_tag(platform=platform, registry=registry)
    logging.info("Building container tagged '%s' with %s", tag, docker_binary)
    cmd = [docker_binary, 'build', '-f', get_dockerfile(platform), '--build-arg', 'USER_ID={}'.format(os.getuid()), '--cache-from', tag, '-t', tag, 'docker']
    logging.info("Running command: '%s'", ' '.join(cmd))
    check_call(cmd)
    image_id = _get_local_image_id(docker_binary=docker_binary, docker_tag=tag)
    if (not image_id):
        raise FileNotFoundError('Unable to find docker image id matching with {}'.format(tag))
    return image_id