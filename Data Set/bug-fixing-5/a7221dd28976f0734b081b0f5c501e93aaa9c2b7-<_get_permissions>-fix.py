def _get_permissions(self):
    perms_out = [perm for perm in self._exec(['list_user_permissions', self.username], True) if perm.strip()]
    perms_list = list()
    for perm in perms_out:
        (vhost, configure_priv, write_priv, read_priv) = perm.split('\t')
        if (not self.bulk_permissions):
            if (vhost == self.permissions[0]['vhost']):
                perms_list.append(dict(vhost=vhost, configure_priv=configure_priv, write_priv=write_priv, read_priv=read_priv))
                break
        else:
            perms_list.append(dict(vhost=vhost, configure_priv=configure_priv, write_priv=write_priv, read_priv=read_priv))
    return perms_list