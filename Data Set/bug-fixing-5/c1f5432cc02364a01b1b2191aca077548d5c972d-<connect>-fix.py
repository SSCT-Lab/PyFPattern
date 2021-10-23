def connect(self):
    try:
        self.omapi = Omapi(self.module.params['host'], self.module.params['port'], self.module.params['key_name'], self.module.params['key'])
    except binascii.Error:
        self.module.fail_json(msg="Unable to open OMAPI connection. 'key' is not a valid base64 key.")
    except OmapiError:
        e = get_exception()
        self.module.fail_json(msg=("Unable to open OMAPI connection. Ensure 'host', 'port', 'key' and 'key_name' are valid. Exception was: %s" % e))
    except socket.error:
        e = get_exception()
        self.module.fail_json(msg=('Unable to connect to OMAPI server: %s' % e))