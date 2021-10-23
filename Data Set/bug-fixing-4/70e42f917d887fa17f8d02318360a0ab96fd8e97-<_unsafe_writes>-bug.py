def _unsafe_writes(self, src, dest):
    try:
        try:
            out_dest = open(dest, 'wb')
            in_src = open(src, 'rb')
            shutil.copyfileobj(in_src, out_dest)
        finally:
            if out_dest:
                out_dest.close()
            if in_src:
                in_src.close()
    except (shutil.Error, OSError, IOError):
        e = get_exception()
        self.fail_json(msg=('Could not write data to file (%s) from (%s): %s' % (dest, src, e)))