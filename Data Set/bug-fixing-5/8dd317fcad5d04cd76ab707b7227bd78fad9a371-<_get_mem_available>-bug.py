def _get_mem_available():
    '\n    Get information about memory available, not counting swap.\n    '
    try:
        import psutil
        return psutil.virtual_memory().available
    except (ImportError, AttributeError):
        pass
    if sys.platform.startswith('linux'):
        info = {
            
        }
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                p = line.split()
                info[p[0].strip(':').lower()] = (float(p[1]) * 1000.0)
        if ('memavailable' in info):
            return info['memavailable']
        else:
            return (info['memfree'] + info['memcached'])
    return None