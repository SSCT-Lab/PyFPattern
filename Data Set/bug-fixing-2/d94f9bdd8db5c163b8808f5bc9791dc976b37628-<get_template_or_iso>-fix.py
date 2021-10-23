

def get_template_or_iso(self, key=None):
    template = self.module.params.get('template')
    iso = self.module.params.get('iso')
    if ((not template) and (not iso)):
        return None
    args = {
        
    }
    args['account'] = self.get_account(key='name')
    args['domainid'] = self.get_domain(key='id')
    args['projectid'] = self.get_project(key='id')
    args['zoneid'] = self.get_zone(key='id')
    args['isrecursive'] = True
    if template:
        if self.template:
            return self._get_by_key(key, self.template)
        rootdisksize = self.module.params.get('root_disk_size')
        args['templatefilter'] = self.module.params.get('template_filter')
        templates = self.cs.listTemplates(**args)
        if templates:
            for t in templates['template']:
                if (template in [t['displaytext'], t['name'], t['id']]):
                    if (rootdisksize and (t['size'] > (rootdisksize * (1024 ** 3)))):
                        continue
                    self.template = t
                    return self._get_by_key(key, self.template)
        more_info = ''
        if rootdisksize:
            more_info = (' (with size <= %s)' % rootdisksize)
        self.module.fail_json(msg=("Template '%s' not found%s" % (template, more_info)))
    elif iso:
        if self.iso:
            return self._get_by_key(key, self.iso)
        args['isofilter'] = self.module.params.get('template_filter')
        isos = self.cs.listIsos(**args)
        if isos:
            for i in isos['iso']:
                if (iso in [i['displaytext'], i['name'], i['id']]):
                    self.iso = i
                    return self._get_by_key(key, self.iso)
        self.module.fail_json(msg=("ISO '%s' not found" % iso))
