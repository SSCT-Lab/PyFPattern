

def filter_list(s3, bucket, s3filelist, strategy):
    keeplist = list(s3filelist)
    for e in keeplist:
        e['_strategy'] = strategy
    if (not (strategy == 'force')):
        keeplist = head_s3(s3, bucket, s3filelist)
    if (strategy == 'checksum'):
        for entry in keeplist:
            if entry.get('s3_head'):
                if (entry['s3_head']['ETag'] == entry['local_etag']):
                    entry['skip_flag'] = True
                else:
                    pass
            else:
                pass
    elif (strategy == 'date_size'):
        for entry in keeplist:
            if entry.get('s3_head'):
                local_modified_epoch = entry['modified_epoch']
                local_size = entry['bytes']
                remote_modified_datetime = entry['s3_head']['LastModified']
                delta = (remote_modified_datetime - datetime.datetime(1970, 1, 1, tzinfo=tz.tzutc()))
                remote_modified_epoch = (delta.seconds + (delta.days * 86400))
                remote_size = entry['s3_head']['ContentLength']
                entry['whytime'] = '{0} / {1}'.format(local_modified_epoch, remote_modified_epoch)
                entry['whysize'] = '{0} / {1}'.format(local_size, remote_size)
                if ((local_modified_epoch <= remote_modified_epoch) and (local_size == remote_size)):
                    entry['skip_flag'] = True
            else:
                entry['why'] = 'no s3_head'
    else:
        pass
    return [x for x in keeplist if (not x.get('skip_flag'))]
