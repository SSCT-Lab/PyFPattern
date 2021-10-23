def set(self, key, value):
    self._cache[key] = value
    cachefile = ('%s/%s' % (self._cache_dir, key))
    try:
        f = codecs.open(cachefile, 'w', encoding='utf-8')
    except (OSError, IOError) as e:
        display.warning(('error while trying to write to %s : %s' % (cachefile, to_bytes(e))))
        pass
    else:
        f.write(jsonify(value, format=True))
    finally:
        try:
            f.close()
        except UnboundLocalError:
            pass