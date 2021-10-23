def account_obj_to_dict(self, account_obj):
    account_dict = dict(id=account_obj.id, name=account_obj.name, location=account_obj.location, resource_group=self.resource_group, type=account_obj.type, access_tier=(account_obj.access_tier.value if (account_obj.access_tier is not None) else None), sku_tier=account_obj.sku.tier.value, sku_name=account_obj.sku.name.value, provisioning_state=account_obj.provisioning_state.value, secondary_location=account_obj.secondary_location, status_of_primary=(account_obj.status_of_primary.value if (account_obj.status_of_primary is not None) else None), status_of_secondary=(account_obj.status_of_secondary.value if (account_obj.status_of_secondary is not None) else None), primary_location=account_obj.primary_location)
    account_dict['custom_domain'] = None
    if account_obj.custom_domain:
        account_dict['custom_domain'] = dict(name=account_obj.custom_domain.name, use_sub_domain=account_obj.custom_domain.use_sub_domain)
    account_dict['primary_endpoints'] = None
    if account_obj.primary_endpoints:
        account_dict['primary_endpoints'] = dict(blob=account_obj.primary_endpoints.blob, queue=account_obj.primary_endpoints.queue, table=account_obj.primary_endpoints.table)
    account_dict['secondary_endpoints'] = None
    if account_obj.secondary_endpoints:
        account_dict['secondary_endpoints'] = dict(blob=account_obj.secondary_endpoints.blob, queue=account_obj.secondary_endpoints.queue, table=account_obj.secondary_endpoints.table)
    account_dict['tags'] = None
    if account_obj.tags:
        account_dict['tags'] = account_obj.tags
    return account_dict