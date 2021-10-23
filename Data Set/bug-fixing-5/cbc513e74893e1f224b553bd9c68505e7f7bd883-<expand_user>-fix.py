def expand_user(self, user_home_path, username=''):
    ' Return a command to expand tildes in a path\n\n        It can be either "~" or "~username". We just ignore $HOME\n        We use the POSIX definition of a username:\n            http://pubs.opengroup.org/onlinepubs/000095399/basedefs/xbd_chap03.html#tag_03_426\n            http://pubs.opengroup.org/onlinepubs/000095399/basedefs/xbd_chap03.html#tag_03_276\n\n            Falls back to \'current working directory\' as we assume \'home is where the remote user ends up\'\n        '
    if (user_home_path != '~'):
        if (not _USER_HOME_PATH_RE.match(user_home_path)):
            user_home_path = shlex_quote(user_home_path)
    elif username:
        user_home_path += username
    return ('echo %s' % user_home_path)