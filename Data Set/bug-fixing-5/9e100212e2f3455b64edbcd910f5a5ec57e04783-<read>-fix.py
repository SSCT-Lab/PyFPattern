def read(self):
    '\n        Read in the pg_hba from the system\n        '
    self.rules = {
        
    }
    self.comment = []
    try:
        file = open(self.pg_hba_file, 'r')
        for line in file:
            line = line.strip()
            if ('#' in line):
                (line, comment) = line.split('#', 1)
                self.comment.append(('#' + comment))
            try:
                self.add_rule(PgHbaRule(line=line, order=self.order))
            except PgHbaRuleError:
                pass
        file.close()
        self.unchanged()
    except IOError:
        pass