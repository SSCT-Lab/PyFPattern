def gather_host_facts(self):
    hosts_facts = {
        
    }
    for host in self.hosts:
        host_service_facts = []
        host_service_system = host.configManager.serviceSystem
        if host_service_system:
            services = host_service_system.serviceInfo.service
            for service in services:
                host_service_facts.append(dict(key=service.key, label=service.label, required=service.required, uninstallable=service.uninstallable, running=service.running, policy=service.policy, source_package_name=(service.sourcePackage.sourcePackageName if service.sourcePackage else 'NA'), source_package_desc=(service.sourcePackage.description if service.sourcePackage else 'NA')))
        hosts_facts[host.name] = host_service_facts
    return hosts_facts