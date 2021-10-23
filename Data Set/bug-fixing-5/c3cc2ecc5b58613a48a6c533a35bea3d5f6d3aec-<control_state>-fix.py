def control_state(sd_module):
    sd = sd_module.search_entity()
    if (sd is None):
        return
    sd_service = sd_module._service.service(sd.id)
    if (sd.status is None):
        sd_service = sd_module._attached_sd_service(sd)
        sd = get_entity(sd_service)
    if (sd.status == sdstate.LOCKED):
        wait(service=sd_service, condition=(lambda sd: (sd.status != sdstate.LOCKED)), fail_condition=failed_state)
    if failed_state(sd):
        raise Exception(("Not possible to manage storage domain '%s'." % sd.name))
    elif (sd.status == sdstate.ACTIVATING):
        wait(service=sd_service, condition=(lambda sd: (sd.status == sdstate.ACTIVE)), fail_condition=failed_state)
    elif (sd.status == sdstate.DETACHING):
        wait(service=sd_service, condition=(lambda sd: (sd.status == sdstate.UNATTACHED)), fail_condition=failed_state)
    elif (sd.status == sdstate.PREPARING_FOR_MAINTENANCE):
        wait(service=sd_service, condition=(lambda sd: (sd.status == sdstate.MAINTENANCE)), fail_condition=failed_state)