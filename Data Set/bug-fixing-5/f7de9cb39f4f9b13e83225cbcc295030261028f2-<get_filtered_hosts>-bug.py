def get_filtered_hosts(cluster_version, hosts):
    filtered_hosts = []
    for host in hosts:
        cluster = host.cluster
        cluster_version_host = ((str(cluster.version.major) + '.') + str(cluster.version.minor))
        if (cluster_version_host == cluster_version):
            filtered_hosts.append(host)
    return filtered_hosts