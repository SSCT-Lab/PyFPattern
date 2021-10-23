def create_account(self):
    '\n        Create the Account\n        '
    try:
        self.sfe.add_account(username=self.element_username, initiator_secret=self.initiator_secret, target_secret=self.target_secret, attributes=self.attributes)
    except Exception as e:
        self.module.fail_json(msg=('Error creating account %s: %s' % (self.element_username, to_native(e))), exception=traceback.format_exc())