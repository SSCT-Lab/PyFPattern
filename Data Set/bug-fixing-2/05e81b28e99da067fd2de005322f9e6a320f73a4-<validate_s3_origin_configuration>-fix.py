

def validate_s3_origin_configuration(self, client, existing_config, origin):
    if (origin['s3_origin_access_identity_enabled'] and existing_config.get('s3_origin_config', {
        
    }).get('origin_access_identity')):
        return existing_config['s3_origin_config']['origin_access_identity']
    if (not origin['s3_origin_access_identity_enabled']):
        return None
    try:
        comment = ('access-identity-by-ansible-%s-%s' % (origin.get('domain_name'), self.__default_datetime_string))
        caller_reference = ('%s-%s' % (origin.get('domain_name'), self.__default_datetime_string))
        cfoai_config = dict(CloudFrontOriginAccessIdentityConfig=dict(CallerReference=caller_reference, Comment=comment))
        oai = client.create_cloud_front_origin_access_identity(**cfoai_config)['CloudFrontOriginAccessIdentity']['Id']
    except Exception as e:
        self.module.fail_json_aws(e, msg=("Couldn't create Origin Access Identity for id %s" % origin['id']))
    return ('origin-access-identity/cloudfront/%s' % oai)
