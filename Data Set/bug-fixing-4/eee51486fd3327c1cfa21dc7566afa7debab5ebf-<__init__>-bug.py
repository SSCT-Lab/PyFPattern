def __init__(self):
    argument_spec = eseries_host_argument_spec()
    argument_spec.update(dict(name=dict(type='str', required=False, aliases=['alias']), ping=dict(type='bool', required=False, default=True), chap_secret=dict(type='str', required=False, aliases=['chap', 'password'], no_log=True), unnamed_discovery=dict(type='bool', required=False, default=True), log_path=dict(type='str', required=False)))
    self.module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    args = self.module.params
    self.name = args['name']
    self.ping = args['ping']
    self.chap_secret = args['chap_secret']
    self.unnamed_discovery = args['unnamed_discovery']
    self.ssid = args['ssid']
    self.url = args['api_url']
    self.creds = dict(url_password=args['api_password'], validate_certs=args['validate_certs'], url_username=args['api_username'])
    self.check_mode = self.module.check_mode
    self.post_body = dict()
    self.controllers = list()
    log_path = args['log_path']
    self._logger = logging.getLogger(self.__class__.__name__)
    if log_path:
        logging.basicConfig(level=logging.DEBUG, filename=log_path, filemode='w', format='%(relativeCreated)dms %(levelname)s %(module)s.%(funcName)s:%(lineno)d\n %(message)s')
    if (not self.url.endswith('/')):
        self.url += '/'
    self._logger.info(self.chap_secret)
    if (self.chap_secret is not None):
        if ((len(self.chap_secret) < 12) or (len(self.chap_secret) > 16)):
            self.module.fail_json(msg='The provided CHAP secret is not valid, it must be between 12 and 16 characters in length.')
        for c in self.chap_secret:
            ordinal = ord(c)
            if ((ordinal < 32) or (ordinal > 126)):
                self.module.fail_json(msg='The provided CHAP secret is not valid, it may only utilize ascii characters with decimal values between 32 and 126.')