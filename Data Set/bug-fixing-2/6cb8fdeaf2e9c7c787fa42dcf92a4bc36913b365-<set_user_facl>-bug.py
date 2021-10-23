

def set_user_facl(self, path, user, mode, recursive=True):
    "Only sets acls for users as that's really all we need"
    path = pipes.quote(path)
    mode = pipes.quote(mode)
    user = pipes.quote(user)
    cmd = ['setfacl']
    if recursive:
        cmd.append('-R')
    cmd.extend(('-m', ('u:%s:%s %s' % (user, mode, path))))
    return ' '.join(cmd)
