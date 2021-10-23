def get_checksum(self, dest, all_vars, try_directory=False, source=None, tmp=None):
    try:
        dest_stat = self._execute_remote_stat(dest, all_vars=all_vars, follow=False, tmp=tmp)
        if (dest_stat['exists'] and dest_stat['isdir'] and try_directory and source):
            base = os.path.basename(source)
            dest = os.path.join(dest, base)
            dest_stat = self._execute_remote_stat(dest, all_vars=all_vars, follow=False, tmp=tmp)
    except AnsibleError as e:
        return dict(failed=True, msg=to_text(e))
    return dest_stat['checksum']