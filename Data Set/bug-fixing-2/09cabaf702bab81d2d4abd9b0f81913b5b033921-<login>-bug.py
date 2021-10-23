

def login(self):
    service_type = self.params['service_type']
    password = self.params['password']
    login_org = None
    if (service_type == 'vcd'):
        login_org = self.params['org']
    if (not self.vca.login(password=password, org=login_org)):
        self.fail('Login to VCA failed', response=self.vca.response)
    try:
        method_name = ('login_%s' % service_type)
        meth = getattr(self, method_name)
        meth()
    except AttributeError:
        self.fail(('no login method exists for service_type %s' % service_type))
    except VcaError as e:
        self.fail(e.message, response=self.vca.response, **e.kwargs)
