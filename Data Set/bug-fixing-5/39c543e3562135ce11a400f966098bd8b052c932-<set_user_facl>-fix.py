def set_user_facl(self, path, user, mode, recursive=True):
    "Only sets acls for users as that's really all we need"
    path = pipes.quote(path)
    mode = pipes.quote(mode)
    user = pipes.quote(user)
    cmd = ['setfacl', '-m', ('u:%s:%s' % (user, mode))]
    if recursive:
        cmd = ((['find', path, '-exec'] + cmd) + ["'{}'", "'+'"])
    else:
        cmd.append(path)
    return ' '.join(cmd)