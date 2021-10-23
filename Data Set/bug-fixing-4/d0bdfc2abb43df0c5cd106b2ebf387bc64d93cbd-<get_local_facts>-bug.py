def get_local_facts(self):
    fact_path = self.module.params.get('fact_path', None)
    if ((not fact_path) or (not os.path.exists(fact_path))):
        return
    local = {
        
    }
    for fn in sorted(glob.glob((fact_path + '/*.fact'))):
        fact_base = os.path.basename(fn).replace('.fact', '')
        if (stat.S_IXUSR & os.stat(fn)[stat.ST_MODE]):
            (rc, out, err) = self.module.run_command(fn)
            try:
                out = out.decode('utf-8', 'strict')
            except UnicodeError:
                fact = ('error loading fact - output of running %s was not utf-8' % fn)
                local[fact_base] = fact
                self.facts['local'] = local
                return
        else:
            out = get_file_content(fn, default='')
        fact = ('loading %s' % fact_base)
        try:
            fact = json.loads(out)
        except ValueError:
            cp = configparser.ConfigParser()
            try:
                cp.readfp(StringIO(out))
            except configparser.Error:
                fact = 'error loading fact - please check content'
            else:
                fact = {
                    
                }
                for sect in cp.sections():
                    if (sect not in fact):
                        fact[sect] = {
                            
                        }
                    for opt in cp.options(sect):
                        val = cp.get(sect, opt)
                        fact[sect][opt] = val
        local[fact_base] = fact
    if (not local):
        return
    self.facts['local'] = local