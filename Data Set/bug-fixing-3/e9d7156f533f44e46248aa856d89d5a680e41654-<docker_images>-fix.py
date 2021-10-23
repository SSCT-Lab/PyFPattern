def docker_images(args, image):
    '\n    :param args: CommonConfig\n    :param image: str\n    :rtype: list[dict[str, any]]\n    '
    try:
        (stdout, _dummy) = docker_command(args, ['images', image, '--format', '{{json .}}'], capture=True, always=True)
    except SubprocessError as ex:
        if ('no such image' in ex.stderr):
            stdout = ''
        else:
            raise ex
    results = [json.loads(line) for line in stdout.splitlines()]
    return results