def get_raw(self, item_id, vault=None):
    try:
        args = ['get', 'item', item_id]
        if (vault is not None):
            args += ['--vault={0}'.format(vault)]
        if (not self.logged_in):
            args += [(to_bytes('--session=') + self.token)]
        (rc, output, dummy) = self._run(args)
        return output
    except Exception as e:
        if re.search('.*not found.*', to_native(e)):
            module.fail_json(msg=("Unable to find an item in 1Password named '%s'." % item_id))
        else:
            module.fail_json(msg=("Unexpected error attempting to find an item in 1Password named '%s': %s" % (item_id, to_native(e))))