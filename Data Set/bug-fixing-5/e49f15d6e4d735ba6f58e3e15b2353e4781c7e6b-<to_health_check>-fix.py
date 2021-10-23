def to_health_check(config):
    return HealthCheck(config.get('IPAddress'), int(config.get('Port')), config.get('Type'), config.get('ResourcePath'), fqdn=config.get('FullyQualifiedDomainName'), string_match=config.get('SearchString'), request_interval=int(config.get('RequestInterval')), failure_threshold=int(config.get('FailureThreshold')))