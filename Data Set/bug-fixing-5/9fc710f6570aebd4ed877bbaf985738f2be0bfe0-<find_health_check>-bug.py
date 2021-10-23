def find_health_check(conn, wanted):
    'Searches for health checks that have the exact same set of immutable values'
    for check in conn.get_list_health_checks().HealthChecks:
        config = check.HealthCheckConfig
        if ((config.get('IPAddress') == wanted.ip_addr) and (config.get('FullyQualifiedDomainName') == wanted.fqdn) and (config.get('Type') == wanted.hc_type) and (config.get('RequestInterval') == str(wanted.request_interval)) and (config.get('Port') == str(wanted.port))):
            return check
    return None