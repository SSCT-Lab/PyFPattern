

def _build_save_container(platform, registry, load_cache) -> Optional[str]:
    '\n    Build image for passed platform and upload the cache to the specified S3 bucket\n    :param platform: Platform\n    :param registry: Docker registry name\n    :param load_cache: Load cache before building\n    :return: Platform if failed, None otherwise\n    '
    docker_tag = build_util.get_docker_tag(platform=platform, registry=registry)
    if load_cache:
        load_docker_cache(registry=registry, docker_tag=docker_tag)
    logging.debug('Building %s as %s', platform, docker_tag)
    try:
        image_id = build_util.build_docker(docker_binary='docker', platform=platform, registry=registry, num_retries=10, use_cache=True)
        logging.info('Built %s as %s', docker_tag, image_id)
        _upload_image(registry=registry, docker_tag=docker_tag, image_id=image_id)
        return None
    except Exception:
        logging.exception('Unexpected exception during build of %s', docker_tag)
        return platform
