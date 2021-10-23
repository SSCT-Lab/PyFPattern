def apply(self):
    '\n        Process the account operation on the Element OS Cluster\n        '
    changed = False
    account_exists = False
    update_account = False
    account_detail = self.get_account()
    if account_detail:
        account_exists = True
        if (self.state == 'absent'):
            changed = True
        elif (self.state == 'present'):
            if ((account_detail.username is not None) and (self.new_element_username is not None) and (account_detail.username != self.new_element_username)):
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
    elif ((self.state == 'present') and (self.status is None)):
        changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not account_exists):
                self.create_account()
            elif update_account:
                self.update_account()
        elif (self.state == 'absent'):
            self.delete_account()
    self.module.exit_json(changed=changed)