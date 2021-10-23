def __get_pretty_val(self, setting):
    return self.__exec_sql(('SHOW %s' % setting))[0][0]