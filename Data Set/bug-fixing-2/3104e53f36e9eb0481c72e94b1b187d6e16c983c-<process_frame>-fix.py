

def process_frame(self, processable_frame, processing_task):
    frame = processable_frame.frame
    raw_frame = dict(frame)
    errors = []
    if (raw_frame.get('package') is None):
        obj = processable_frame.data['obj']
        raw_frame['package'] = ((obj and obj.code_file) or None)
    if (processable_frame.cache_value is None):
        instruction_addr = processable_frame.data['instruction_addr']
        debug_id = processable_frame.data['debug_id']
        if (debug_id is not None):
            self.difs_referenced.add(debug_id)
        try:
            symbolicated_frames = self.sym.symbolize_frame(instruction_addr, self.sdk_info, symbolserver_match=processable_frame.data['symbolserver_match'], symbolicator_match=processable_frame.data.get('symbolicator_match'), trust=raw_frame.get('trust'))
            if (not symbolicated_frames):
                if (raw_frame.get('trust') == 'scan'):
                    return ([], [raw_frame], [])
                else:
                    return (None, [raw_frame], [])
        except SymbolicationFailed as e:
            errors = self._handle_symbolication_failed(e)
            return ([raw_frame], [raw_frame], errors)
        _ignored = None
        processable_frame.set_cache_value([_ignored, symbolicated_frames])
    else:
        (_ignored, symbolicated_frames) = processable_frame.cache_value
    new_frames = []
    for sfrm in symbolicated_frames:
        new_frame = dict(raw_frame)
        new_frame['function'] = sfrm['function']
        if sfrm.get('symbol'):
            new_frame['symbol'] = sfrm['symbol']
        if sfrm.get('abs_path'):
            new_frame['abs_path'] = sfrm['abs_path']
            new_frame['filename'] = posixpath.basename(sfrm['abs_path'])
        if sfrm.get('filename'):
            new_frame['filename'] = sfrm['filename']
        if sfrm.get('lineno'):
            new_frame['lineno'] = sfrm['lineno']
        if sfrm.get('colno'):
            new_frame['colno'] = sfrm['colno']
        if sfrm.get('package'):
            new_frame['package'] = sfrm['package']
        new_frames.append(new_frame)
    return (new_frames, [raw_frame], [])
