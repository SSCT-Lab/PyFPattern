def __get_pretty_val(self, setting):
    "\n        Get setting's value represented by SHOW command.\n        "
    return self.__exec_sql(('SHOW %s' % setting))[0][0]