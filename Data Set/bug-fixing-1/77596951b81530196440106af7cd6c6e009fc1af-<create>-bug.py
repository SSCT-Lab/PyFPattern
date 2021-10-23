

def create(module):
    vdc_name = module.params['vdc_name']
    vapp_name = module.params['vapp_name']
    template_name = module.params['template_name']
    catalog_name = module.params['catalog_name']
    network_name = module.params['network_name']
    network_mode = module.params['network_mode']
    vm_name = module.params['vm_name']
    vm_cpus = module.params['vm_cpus']
    vm_memory = module.params['vm_memory']
    deploy = (module.params['state'] == 'deploy')
    poweron = (module.params['operation'] == 'poweron')
    task = module.vca.create_vapp(vdc_name, vapp_name, template_name, catalog_name, network_name, network_mode, vm_name, vm_cpus, vm_memory, deploy, poweron)
    module.vca.block_until_completed(task)
