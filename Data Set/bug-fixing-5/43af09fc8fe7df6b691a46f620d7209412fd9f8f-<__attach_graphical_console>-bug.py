def __attach_graphical_console(self, entity):
    graphical_console = self.param('graphical_console')
    if (not graphical_console):
        return
    vm_service = self._service.service(entity.id)
    gcs_service = vm_service.graphics_consoles_service()
    graphical_consoles = gcs_service.list()
    if bool(graphical_console.get('headless_mode')):
        if (not self._module.check_mode):
            for gc in graphical_consoles:
                gcs_service.console_service(gc.id).remove()
        return (len(graphical_consoles) > 0)
    protocol = graphical_console.get('protocol')
    if isinstance(protocol, str):
        protocol = [protocol]
    current_protocols = [str(gc.protocol) for gc in graphical_consoles]
    if (not current_protocols):
        if (not self._module.check_mode):
            for p in protocol:
                gcs_service.add(otypes.GraphicsConsole(protocol=otypes.GraphicsType(p)))
        return True
    if (sorted(protocol) != sorted(current_protocols)):
        if (not self._module.check_mode):
            for gc in graphical_consoles:
                gcs_service.console_service(gc.id).remove()
            for p in protocol:
                gcs_service.add(otypes.GraphicsConsole(protocol=otypes.GraphicsType(p)))
        return True