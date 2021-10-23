def collect(self, val_list=False):
    subset_map = {
        'version': self.get_pg_version,
        'tablespaces': self.get_tablespaces,
        'databases': self.get_db_info,
        'replications': self.get_repl_info,
        'repl_slots': self.get_rslot_info,
        'settings': self.get_settings,
        'roles': self.get_role_info,
    }
    incl_list = []
    excl_list = []
    if val_list:
        for i in val_list:
            if (i[0] != '!'):
                incl_list.append(i)
            else:
                excl_list.append(i.lstrip('!'))
        if incl_list:
            for s in subset_map:
                for i in incl_list:
                    if fnmatch(s, i):
                        subset_map[s]()
                        break
        elif excl_list:
            found = False
            for s in subset_map:
                for e in excl_list:
                    if fnmatch(s, e):
                        found = True
                if (not found):
                    subset_map[s]()
                else:
                    found = False
    else:
        for s in subset_map:
            subset_map[s]()
    return self.pg_info