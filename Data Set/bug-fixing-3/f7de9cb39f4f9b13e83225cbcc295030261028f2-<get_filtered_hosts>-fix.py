def get_filtered_hosts(cluster_version, hosts, connection):
    filtered_hosts = []
    for host in hosts:
        cluster = connection.follow_link(host.cluster)
        cluster_version_host = ((str(cluster.version.major) + '.') + str(cluster.version.minor))
        if (cluster_version_host == cluster_version):
            filtered_hosts.append(host)
    return filtered_hosts