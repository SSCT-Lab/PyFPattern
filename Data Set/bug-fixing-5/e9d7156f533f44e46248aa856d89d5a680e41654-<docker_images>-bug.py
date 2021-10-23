def docker_images(args, image):
    '\n    :param args: CommonConfig\n    :param image: str\n    :rtype: list[dict[str, any]]\n    '
    (stdout, _dummy) = docker_command(args, ['images', image, '--format', '{{json .}}'], capture=True, always=True)
    results = [json.loads(line) for line in stdout.splitlines()]
    return results