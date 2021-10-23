def validate_distribution_from_caller_reference(self, caller_reference):
    try:
        distributions = self.__cloudfront_facts_mgr.list_distributions(False)
        distribution_name = 'Distribution'
        distribution_config_name = 'DistributionConfig'
        distribution_ids = [dist.get('Id') for dist in distributions]
        for distribution_id in distribution_ids:
            config = self.__cloudfront_facts_mgr.get_distribution(distribution_id)
            distribution = config.get(distribution_name)
            if (distribution is not None):
                distribution_config = distribution.get(distribution_config_name)
                if ((distribution_config is not None) and (distribution_config.get('CallerReference') == caller_reference)):
                    distribution['DistributionConfig'] = distribution_config
                    return distribution
    except Exception as e:
        self.module.fail_json_aws(e, msg='Error validating distribution from caller reference')