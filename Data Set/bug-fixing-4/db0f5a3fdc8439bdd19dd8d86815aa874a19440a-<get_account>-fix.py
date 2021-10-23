def get_account(self, username):
    '\n        Get Account\n            :description: Get Account object from account id or name\n\n            :return: Details about the account. None if not found.\n            :rtype: object (Account object)\n        '
    account_list = self.sfe.list_accounts()
    for account in account_list.accounts:
        if (str(account.account_id) == username):
            return account
        elif (account.username == username):
            return account
    return None