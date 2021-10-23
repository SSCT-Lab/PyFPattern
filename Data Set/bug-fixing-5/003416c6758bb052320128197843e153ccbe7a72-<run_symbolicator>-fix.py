def run_symbolicator(self, processing_task):
    if (not self.available):
        return
    request_id_cache_key = request_id_cache_key_for_event(self.data)
    stacktraces = []
    processable_stacktraces = []
    for (stacktrace_info, pf_list) in processing_task.iter_processable_stacktraces():
        registers = (stacktrace_info.stacktrace.get('registers') or {
            
        })
        pf_list = [pf for pf in reversed(pf_list) if (pf.processor == self)]
        frames = []
        for pf in pf_list:
            frame = {
                'instruction_addr': pf['instruction_addr'],
            }
            if (pf.get('trust') is not None):
                frame['trust'] = pf['trust']
            frames.append(frame)
        stacktraces.append({
            'registers': registers,
            'frames': frames,
        })
        processable_stacktraces.append(pf_list)
    rv = run_symbolicator(stacktraces=stacktraces, modules=self.images, project=self.project, arch=self.arch, signal=self.signal, request_id_cache_key=request_id_cache_key)
    if (not rv):
        self.data.setdefault('errors', []).extend(self._handle_symbolication_failed(SymbolicationFailed(type=EventError.NATIVE_SYMBOLICATOR_FAILED)))
        return
    assert (len(self.images) == len(rv['modules'])), (self.images, rv)
    for (image, fetched_debug_file) in zip(self.images, rv['modules']):
        status = fetched_debug_file.pop('status')
        for (k, v) in six.iteritems(fetched_debug_file):
            if (not ((v is None) or ((k, v) == ('arch', 'unknown')))):
                image[k] = v
        if (status in ('found', 'unused')):
            continue
        elif (status == 'missing_debug_file'):
            package = fetched_debug_file.get('code_file')
            if ((not package) or is_known_third_party(package, sdk_info=self.sdk_info)):
                continue
            if is_optional_package(package, sdk_info=self.sdk_info):
                error = SymbolicationFailed(type=EventError.NATIVE_MISSING_OPTIONALLY_BUNDLED_DSYM)
            else:
                error = SymbolicationFailed(type=EventError.NATIVE_MISSING_DSYM)
        elif (status == 'malformed_debug_file'):
            error = SymbolicationFailed(type=EventError.NATIVE_BAD_DSYM)
        elif (status == 'too_large'):
            error = SymbolicationFailed(type=EventError.FETCH_TOO_LARGE)
        elif (status == 'fetching_failed'):
            error = SymbolicationFailed(type=EventError.FETCH_GENERIC_ERROR)
        elif (status == 'other'):
            error = SymbolicationFailed(type=EventError.UNKNOWN_ERROR)
        else:
            logger.error('Unknown status: %s', status)
            continue
        error.image_arch = image.get('arch')
        error.image_path = image.get('code_file')
        error.image_name = image_name(image.get('code_file'))
        error.image_uuid = image.get('debug_id')
        self.data.setdefault('errors', []).extend(self._handle_symbolication_failed(error))
    assert (len(stacktraces) == len(rv['stacktraces']))
    for (pf_list, symbolicated_stacktrace) in zip(processable_stacktraces, rv['stacktraces']):
        for symbolicated_frame in (symbolicated_stacktrace.get('frames') or ()):
            pf = pf_list[symbolicated_frame['original_index']]
            pf.data['symbolicator_match'].append(symbolicated_frame)