def _override_standard_type_from_profiles(self):
    'Overrides a standard virtual server type given the specified profiles\n\n        For legacy purposes, this module will do some basic overriding of the default\n        ``type`` parameter to support cases where changing the ``type`` only requires\n        specifying a different set of profiles.\n\n        Ideally, ``type`` would always be specified, but in the past, this module only\n        supported an implicit "standard" type. Module users would specify some different\n        types of profiles and this would change the type...in some circumstances.\n\n        Now that this module supports a ``type`` param, the implicit ``type`` changing\n        that used to happen is technically deprecated (and will be warned on). Users\n        should always specify a ``type`` now, or, accept the default standard type.\n\n        Returns:\n            void\n        '
    if (self.want.type == 'standard'):
        if self.want.has_fastl4_profiles:
            self.want.update({
                'type': 'performance-l4',
            })
            self.module.deprecate(msg="Specifying 'performance-l4' profiles on a 'standard' type is deprecated and will be removed.", version='2.10')
        if self.want.has_fasthttp_profiles:
            self.want.update({
                'type': 'performance-http',
            })
            self.module.deprecate(msg="Specifying 'performance-http' profiles on a 'standard' type is deprecated and will be removed.", version='2.10')
        if self.want.has_message_routing_profiles:
            self.want.update({
                'type': 'message-routing',
            })
            self.module.deprecate(msg="Specifying 'message-routing' profiles on a 'standard' type is deprecated and will be removed.", version='2.10')