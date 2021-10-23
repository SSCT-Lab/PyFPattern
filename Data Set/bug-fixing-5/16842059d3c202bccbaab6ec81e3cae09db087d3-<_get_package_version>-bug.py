def _get_package_version(self):
    '\n        Attempt to get the most correct current version of Sentry.\n        '
    pkg_path = os.path.join(self.work_path, 'src')
    sys.path.insert(0, pkg_path)
    try:
        import sentry
    except Exception:
        version = None
        build = None
    else:
        log.info("pulled version information from 'sentry' module".format(sentry.__file__))
        version = self.distribution.get_version()
        build = sentry.__build__
    finally:
        sys.path.pop(0)
    if (not (version and build)):
        try:
            with open(self.get_asset_json_path()) as fp:
                data = json.loads(fp.read())
        except Exception:
            pass
        else:
            log.info("pulled version information from '{}'".format(self.package_path))
            (version, build) = (data['version'], data['build'])
    return {
        'version': version,
        'build': build,
    }