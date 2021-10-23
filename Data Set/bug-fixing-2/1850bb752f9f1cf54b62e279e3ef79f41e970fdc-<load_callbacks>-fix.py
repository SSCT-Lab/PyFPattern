

def load_callbacks(self):
    "\n        Loads all available callbacks, with the exception of those which\n        utilize the CALLBACK_TYPE option. When CALLBACK_TYPE is set to 'stdout',\n        only one such callback plugin will be loaded.\n        "
    if self._callbacks_loaded:
        return
    stdout_callback_loaded = False
    if (self._stdout_callback is None):
        self._stdout_callback = C.DEFAULT_STDOUT_CALLBACK
    if isinstance(self._stdout_callback, CallbackBase):
        stdout_callback_loaded = True
    elif isinstance(self._stdout_callback, string_types):
        if (self._stdout_callback not in callback_loader):
            raise AnsibleError(('Invalid callback for stdout specified: %s' % self._stdout_callback))
        else:
            self._stdout_callback = callback_loader.get(self._stdout_callback)
            try:
                self._stdout_callback.set_options()
            except AttributeError:
                display.deprecated(("%s stdout callback, does not support setting 'options', it will work for now,  but this will be required in the future and should be updated, see the 2.4 porting guide for details." % self._stdout_callback._load_name), version='2.9')
            stdout_callback_loaded = True
    else:
        raise AnsibleError('callback must be an instance of CallbackBase or the name of a callback plugin')
    for callback_plugin in callback_loader.all(class_only=True):
        callback_type = getattr(callback_plugin, 'CALLBACK_TYPE', '')
        callback_needs_whitelist = getattr(callback_plugin, 'CALLBACK_NEEDS_WHITELIST', False)
        (callback_name, _) = os.path.splitext(os.path.basename(callback_plugin._original_path))
        if (callback_type == 'stdout'):
            if ((callback_name != self._stdout_callback) or stdout_callback_loaded):
                continue
            stdout_callback_loaded = True
        elif ((callback_name == 'tree') and self._run_tree):
            pass
        elif ((not self._run_additional_callbacks) or (callback_needs_whitelist and ((C.DEFAULT_CALLBACK_WHITELIST is None) or (callback_name not in C.DEFAULT_CALLBACK_WHITELIST)))):
            continue
        callback_obj = callback_plugin()
        try:
            callback_obj.set_options()
        except AttributeError:
            display.deprecated(("%s callback, does not support setting 'options', it will work for now,  but this will be required in the future and should be updated,  see the 2.4 porting guide for details." % self.callback_obj._load_name), version='2.9')
        self._callback_plugins.append(callback_obj)
    self._callbacks_loaded = True
