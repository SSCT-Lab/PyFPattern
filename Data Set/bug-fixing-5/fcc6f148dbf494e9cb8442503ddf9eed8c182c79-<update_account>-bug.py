def update_account(self):
    self.log('Update storage account {0}'.format(self.name))
    if self.account_type:
        if (self.account_type != self.account_dict['sku_name']):
            if (self.account_dict['sku_name'] in [SkuName.premium_lrs, SkuName.standard_zrs]):
                self.fail('Storage accounts of type {0} and {1} cannot be changed.'.format(SkuName.premium_lrs, SkuName.standard_zrs))
            if (self.account_type in [SkuName.premium_lrs, SkuName.standard_zrs]):
                self.fail('Storage account of type {0} cannot be changed to a type of {1} or {2}.'.format(self.account_dict['sku_name'], SkuName.premium_lrs, SkuName.standard_zrs))
            self.results['changed'] = True
            self.account_dict['sku_name'] = self.account_type
            if (self.results['changed'] and (not self.check_mode)):
                try:
                    self.log(('sku_name: %s' % self.account_dict['sku_name']))
                    self.log(('sku_tier: %s' % self.account_dict['sku_tier']))
                    sku = Sku(SkuName(self.account_dict['sku_name']))
                    sku.tier = SkuTier(self.account_dict['sku_tier'])
                    parameters = StorageAccountUpdateParameters(sku=sku)
                    self.storage_client.storage_accounts.update(self.resource_group, self.name, parameters)
                except Exception as exc:
                    self.fail('Failed to update account type: {0}'.format(str(exc)))
    if self.custom_domain:
        if ((not self.account_dict['custom_domain']) or (self.account_dict['custom_domain'] != self.account_dict['custom_domain'])):
            self.results['changed'] = True
            self.account_dict['custom_domain'] = self.custom_domain
        if (self.results['changed'] and (not self.check_mode)):
            new_domain = CustomDomain(name=self.custom_domain['name'], use_sub_domain=self.custom_domain['use_sub_domain'])
            parameters = StorageAccountUpdateParameters(custom_domain=new_domain)
            try:
                self.storage_client.storage_accounts.update(self.resource_group, self.name, parameters)
            except Exception as exc:
                self.fail('Failed to update custom domain: {0}'.format(str(exc)))
    (update_tags, self.account_dict['tags']) = self.update_tags(self.account_dict['tags'])
    if update_tags:
        self.results['changed'] = True
        if (not self.check_mode):
            parameters = StorageAccountUpdateParameters(tags=self.account_dict['tags'])
            try:
                self.storage_client.storage_accounts.update(self.resource_group, self.name, parameters)
            except Exception as exc:
                self.fail('Failed to update tags: {0}'.format(str(exc)))