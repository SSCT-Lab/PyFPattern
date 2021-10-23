def _init_geoip_rust():
    global rust_geoip
    geoip_path_mmdb = getattr(settings, 'GEOIP_PATH_MMDB', None)
    if (not geoip_path_mmdb):
        logger.warning('No GeoIP MMDB database configured')
        return
    from semaphore.processing import GeoIpLookup
    try:
        rust_geoip = GeoIpLookup.from_path(geoip_path_mmdb)
    except Exception:
        logger.warning(('Error opening GeoIP database in Rust: %s' % geoip_path_mmdb))