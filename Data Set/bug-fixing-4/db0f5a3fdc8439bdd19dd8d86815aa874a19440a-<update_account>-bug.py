def update_account(self):
    '\n        Update the Account\n        '
    try:
        self.sfe.modify_account(account_id=self.account_id, username=self.new_element_username, status=self.status, initiator_secret=self.initiator_secret, target_secret=self.target_secret, attributes=self.attributes)
    except Exception as e:
        self.module.fail_json(msg=('Error updating account %s: %s' % (self.account_id, to_native(e))), exception=traceback.format_exc())