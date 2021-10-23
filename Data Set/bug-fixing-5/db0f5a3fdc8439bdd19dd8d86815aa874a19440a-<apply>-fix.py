def apply(self):
    '\n        Process the account operation on the Element OS Cluster\n        '
    changed = False
    update_account = False
    account_detail = self.get_account(self.element_username)
    if ((account_detail is None) and (self.state == 'present')):
        changed = True
    elif (account_detail is not None):
        self.account_id = account_detail.account_id
        if (self.state == 'absent'):
            changed = True
        elif ((account_detail.username is not None) and (self.element_username is not None) and (account_detail.username != self.element_username)):
            update_account = True
            changed = True
        elif ((account_detail.status is not None) and (self.status is not None) and (account_detail.status != self.status)):
            update_account = True
            changed = True
        elif ((account_detail.initiator_secret is not None) and (self.initiator_secret is not None) and (account_detail.initiator_secret != self.initiator_secret)):
            update_account = True
            changed = True
        elif ((account_detail.target_secret is not None) and (self.target_secret is not None) and (account_detail.target_secret != self.target_secret)):
            update_account = True
            changed = True
        elif ((account_detail.attributes is not None) and (self.attributes is not None) and (account_detail.attributes != self.attributes)):
            update_account = True
            changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if update_account:
                self.update_account()
            elif (self.from_name is not None):
                account_exists = self.get_account(self.from_name)
                if (account_exists is not None):
                    self.account_id = account_exists.account_id
                    self.rename_account()
                else:
                    self.module.fail_json(msg=('Resource does not exist : %s' % self.from_name))
            else:
                self.create_account()
        elif (self.state == 'absent'):
            self.delete_account()
    self.module.exit_json(changed=changed)