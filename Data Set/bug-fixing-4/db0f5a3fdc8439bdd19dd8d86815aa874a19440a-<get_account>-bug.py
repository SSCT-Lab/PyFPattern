def get_account(self):
    '\n        Get Account\n            :description: Get Account object from account id\n\n            :return: Details about the account. None if not found.\n            :rtype: object (Account object)\n        '
    account_list = self.sfe.list_accounts()
    account_obj = None
    for account in account_list.accounts:
        if (account.username == self.element_username):
            if (self.account_id is not None):
                if (account.account_id == self.account_id):
                    account_obj = account
            else:
                self.account_id = account.account_id
                account_obj = account
    return account_obj