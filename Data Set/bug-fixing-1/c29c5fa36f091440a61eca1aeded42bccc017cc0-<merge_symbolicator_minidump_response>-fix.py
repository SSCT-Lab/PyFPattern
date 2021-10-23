

def merge_symbolicator_minidump_response(data, response):
    sdk_info = get_sdk_from_event(data)
    images = []
    set_path(data, 'debug_meta', 'images', value=images)
    for complete_image in response['modules']:
        image = {
            
        }
        merge_symbolicator_image(image, complete_image, sdk_info, (lambda e: handle_symbolication_failed(e, data=data)))
        images.append(image)
    data_threads = []
    data['threads'] = {
        'values': data_threads,
    }
    data_exception = get_path(data, 'exception', 'values', 0)
    for complete_stacktrace in response['stacktraces']:
        is_requesting = complete_stacktrace.get('is_requesting')
        thread_id = complete_stacktrace.get('thread_id')
        data_thread = {
            'id': thread_id,
            'crashed': is_requesting,
        }
        data_threads.append(data_thread)
        if is_requesting:
            data_stacktrace = get_path(data_exception, 'stacktrace')
            assert isinstance(data_stacktrace, dict), data_stacktrace
            if (data_stacktrace['frames'] and is_unreal_exception_stacktrace(data)):
                continue
            del data_stacktrace['frames'][:]
        else:
            data_thread['stacktrace'] = data_stacktrace = {
                'frames': [],
            }
        if complete_stacktrace.get('registers'):
            data_stacktrace['registers'] = complete_stacktrace['registers']
        for complete_frame in reversed(complete_stacktrace['frames']):
            new_frame = {
                
            }
            merge_symbolicated_frame(new_frame, complete_frame)
            data_stacktrace['frames'].append(new_frame)
