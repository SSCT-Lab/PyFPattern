

def fetch_balancer_page(self):
    ' Returns the balancer management html page as a string for later parsing.'
    page = fetch_url(self.module, str(self.url))
    if (page[1]['status'] != 200):
        self.module.fail_json(msg=('Could not get balancer page! HTTP status response: ' + str(page[1]['status'])))
    else:
        content = page[0].read()
        apache_version = regexp_extraction(content.upper(), APACHE_VERSION_EXPRESSION, 1)
        if apache_version:
            if (not re.search(pattern='2\\.4\\.[\\d]*', string=apache_version)):
                self.module.fail_json(msg=('This module only acts on an Apache2 2.4+ instance, current Apache2 version: ' + str(apache_version)))
            return content
        else:
            self.module.fail_json(msg='Could not get the Apache server version from the balancer-manager')
