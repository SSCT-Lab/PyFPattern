

def merge_symbolicated_frame(new_frame, sfrm, platform=None):
    if sfrm.get('function'):
        raw_func = trim(sfrm['function'], 256)
        func = trim(trim_function_name(sfrm['function'], platform), 256)
        if (func == raw_func):
            new_frame['function'] = raw_func
        else:
            new_frame['raw_function'] = raw_func
            new_frame['function'] = func
    if sfrm.get('instruction_addr'):
        new_frame['instruction_addr'] = sfrm['instruction_addr']
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
    if sfrm.get('status'):
        frame_meta = new_frame.setdefault('data', {
            
        })
        frame_meta['symbolicator_status'] = sfrm['status']
