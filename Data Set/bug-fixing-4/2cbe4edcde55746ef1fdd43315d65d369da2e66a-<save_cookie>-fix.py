def save_cookie(self, name, value, domain=None, path='/', expires='Tue, 20 Jun 2025 19:07:44 GMT', max_age=None, secure=None):
    domain = (domain or self.domain)
    if (domain == 'localhost'):
        domain = None
    cookie = {
        'name': name,
        'value': value,
        'expires': expires,
        'path': path,
        'max-age': max_age,
        'secure': secure,
    }
    if domain:
        cookie['domain'] = domain
    if (not self._has_initialized_cookie_store):
        logger.info('selenium.initialize-cookies')
        self.get('/')
    logger.info('selenium.set-cookie.{}'.format(name), extra={
        'value': value,
    })
    if isinstance(self.driver, webdriver.PhantomJS):
        self.driver.execute_script("document.cookie = '{name}={value}; path={path}; domain={domain}; expires={expires}'; max-age={max_age}\n".format(**cookie))
    else:
        del cookie['secure']
        self.driver.add_cookie(cookie)