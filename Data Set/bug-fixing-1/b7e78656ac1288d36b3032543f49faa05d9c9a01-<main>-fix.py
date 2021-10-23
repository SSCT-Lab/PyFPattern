

def main():
    module = AnsibleModule(argument_spec=dict(allowed=dict(), ipv4_range=dict(), fwname=dict(), name=dict(), src_range=dict(type='list'), src_tags=dict(type='list'), target_tags=dict(type='list'), state=dict(default='present'), service_account_email=dict(), pem_file=dict(), credentials_file=dict(), project_id=dict(), mode=dict(default='legacy', choices=['legacy', 'auto', 'custom']), subnet_name=dict(), subnet_region=dict(), subnet_desc=dict()))
    if (not HAS_LIBCLOUD):
        module.fail_json(msg='libcloud with GCE support (0.17.0+) required for this module')
    gce = gce_connect(module)
    allowed = module.params.get('allowed')
    ipv4_range = module.params.get('ipv4_range')
    fwname = module.params.get('fwname')
    name = module.params.get('name')
    src_range = module.params.get('src_range')
    src_tags = module.params.get('src_tags')
    target_tags = module.params.get('target_tags')
    state = module.params.get('state')
    mode = module.params.get('mode')
    subnet_name = module.params.get('subnet_name')
    subnet_region = module.params.get('subnet_region')
    subnet_desc = module.params.get('subnet_desc')
    changed = False
    json_output = {
        'state': state,
    }
    if (state in ['active', 'present']):
        network = None
        subnet = None
        try:
            network = gce.ex_get_network(name)
            json_output['name'] = name
            if (mode == 'legacy'):
                json_output['ipv4_range'] = network.cidr
            if (network and (mode == 'custom') and subnet_name):
                if (not hasattr(gce, 'ex_get_subnetwork')):
                    module.fail_json(msg="Update libcloud to a more recent version (>1.0) that supports network 'mode' parameter", changed=False)
                subnet = gce.ex_get_subnetwork(subnet_name, region=subnet_region)
                json_output['subnet_name'] = subnet_name
                json_output['ipv4_range'] = subnet.cidr
        except ResourceNotFoundError:
            pass
        except Exception as e:
            module.fail_json(msg=unexpected_error_msg(e), changed=False)
        if (name and (not network)):
            if ((not ipv4_range) and (mode != 'auto')):
                module.fail_json(msg=(("Network '" + name) + "' is not found. To create network in legacy or custom mode, 'ipv4_range' parameter is required"), changed=False)
            args = [(ipv4_range if (mode == 'legacy') else None)]
            kwargs = {
                
            }
            if (mode != 'legacy'):
                kwargs['mode'] = mode
            try:
                network = gce.ex_create_network(name, *args, **kwargs)
                json_output['name'] = name
                json_output['ipv4_range'] = ipv4_range
                changed = True
            except TypeError:
                module.fail_json(msg="Update libcloud to a more recent version (>1.0) that supports network 'mode' parameter", changed=False)
            except Exception as e:
                module.fail_json(msg=unexpected_error_msg(e), changed=False)
        if ((subnet_name or ipv4_range) and (not subnet) and (mode == 'custom')):
            if (not hasattr(gce, 'ex_create_subnetwork')):
                module.fail_json(msg='Update libcloud to a more recent version (>1.0) that supports subnetwork creation', changed=changed)
            if ((not subnet_name) or (not ipv4_range) or (not subnet_region)):
                module.fail_json(msg='subnet_name, ipv4_range, and subnet_region required for custom mode', changed=changed)
            try:
                subnet = gce.ex_create_subnetwork(subnet_name, cidr=ipv4_range, network=name, region=subnet_region, description=subnet_desc)
                json_output['subnet_name'] = subnet_name
                json_output['ipv4_range'] = ipv4_range
                changed = True
            except Exception as e:
                module.fail_json(msg=unexpected_error_msg(e), changed=changed)
        if fwname:
            if ((not allowed) and (not src_range) and (not src_tags)):
                if (changed and network):
                    module.fail_json(msg=('Network created, but missing required ' + 'firewall rule parameter(s)'), changed=True)
                module.fail_json(msg='Missing required firewall rule parameter(s)', changed=False)
            allowed_list = format_allowed(allowed)
            try:
                fw_changed = False
                fw = gce.ex_get_firewall(fwname)
                if (allowed_list and (sorted_allowed_list(allowed_list) != sorted_allowed_list(fw.allowed))):
                    fw.allowed = allowed_list
                    fw_changed = True
                fw.source_ranges = (fw.source_ranges or [])
                if (fw.source_ranges != src_range):
                    if isinstance(src_range, list):
                        if (sorted(fw.source_ranges) != sorted(src_range)):
                            fw.source_ranges = src_range
                            fw_changed = True
                    else:
                        fw.source_ranges = src_range
                        fw_changed = True
                fw.source_tags = (fw.source_tags or [])
                if (fw.source_tags != src_tags):
                    if isinstance(src_tags, list):
                        if (sorted(fw.source_tags) != sorted(src_tags)):
                            fw.source_tags = src_tags
                            fw_changed = True
                    else:
                        fw.source_tags = src_tags
                        fw_changed = True
                fw.target_tags = (fw.target_tags or [])
                if (fw.target_tags != target_tags):
                    if isinstance(target_tags, list):
                        if (sorted(fw.target_tags) != sorted(target_tags)):
                            fw.target_tags = target_tags
                            fw_changed = True
                    else:
                        fw.target_tags = target_tags
                        fw_changed = True
                if (fw_changed is True):
                    try:
                        gce.ex_update_firewall(fw)
                        changed = True
                    except Exception as e:
                        module.fail_json(msg=unexpected_error_msg(e), changed=False)
            except ResourceNotFoundError:
                try:
                    gce.ex_create_firewall(fwname, allowed_list, network=name, source_ranges=src_range, source_tags=src_tags, target_tags=target_tags)
                    changed = True
                except Exception as e:
                    module.fail_json(msg=unexpected_error_msg(e), changed=False)
            except Exception as e:
                module.fail_json(msg=unexpected_error_msg(e), changed=False)
            json_output['fwname'] = fwname
            json_output['allowed'] = allowed
            json_output['src_range'] = src_range
            json_output['src_tags'] = src_tags
            json_output['target_tags'] = target_tags
    if (state in ['absent', 'deleted']):
        if fwname:
            json_output['fwname'] = fwname
            fw = None
            try:
                fw = gce.ex_get_firewall(fwname)
            except ResourceNotFoundError:
                pass
            except Exception as e:
                module.fail_json(msg=unexpected_error_msg(e), changed=False)
            if fw:
                gce.ex_destroy_firewall(fw)
                changed = True
        elif subnet_name:
            if ((not hasattr(gce, 'ex_get_subnetwork')) or (not hasattr(gce, 'ex_destroy_subnetwork'))):
                module.fail_json(msg='Update libcloud to a more recent version (>1.0) that supports subnetwork creation', changed=changed)
            json_output['name'] = subnet_name
            subnet = None
            try:
                subnet = gce.ex_get_subnetwork(subnet_name, region=subnet_region)
            except ResourceNotFoundError:
                pass
            except Exception as e:
                module.fail_json(msg=unexpected_error_msg(e), changed=False)
            if subnet:
                gce.ex_destroy_subnetwork(subnet)
                changed = True
        elif name:
            json_output['name'] = name
            network = None
            try:
                network = gce.ex_get_network(name)
            except ResourceNotFoundError:
                pass
            except Exception as e:
                module.fail_json(msg=unexpected_error_msg(e), changed=False)
            if network:
                try:
                    gce.ex_destroy_network(network)
                except Exception as e:
                    module.fail_json(msg=unexpected_error_msg(e), changed=False)
                changed = True
    json_output['changed'] = changed
    module.exit_json(**json_output)
