def get_docker_tag(platform: str, registry: str) -> str:
    return '{0}/build.{1}'.format(registry, platform)