def _user_attr_info(self):
    info = ([''] * 3)
    with open(self.USER_ATTR, 'r') as file_handler:
        for line in file_handler:
            lines = line.strip().split('::::')
            if (lines[0] == self.name):
                tmp = dict((x.split('=') for x in lines[1].split(';')))
                info[0] = tmp.get('profiles', '')
                info[1] = tmp.get('auths', '')
                info[2] = tmp.get('roles', '')
    return info