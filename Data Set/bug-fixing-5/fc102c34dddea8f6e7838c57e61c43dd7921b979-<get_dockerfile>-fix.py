def get_dockerfile(platform: str, path='docker') -> str:
    return os.path.join(path, 'Dockerfile.build.{0}'.format(platform))