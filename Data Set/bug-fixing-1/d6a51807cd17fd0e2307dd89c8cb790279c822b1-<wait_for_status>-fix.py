

def wait_for_status(client, stream_name, status, wait_timeout=300, check_mode=False):
    "Wait for the status to change for a Kinesis Stream.\n    Args:\n        client (botocore.client.EC2): Boto3 client\n        stream_name (str): The name of the kinesis stream.\n        status (str): The status to wait for.\n            examples. status=available, status=deleted\n\n    Kwargs:\n        wait_timeout (int): Number of seconds to wait, until this timeout is reached.\n        check_mode (bool): This will pass DryRun as one of the parameters to the aws api.\n            default=False\n\n    Basic Usage:\n        >>> client = boto3.client('kinesis')\n        >>> stream_name = 'test-stream'\n        >>> wait_for_status(client, stream_name, 'ACTIVE', 300)\n\n    Returns:\n        Tuple (bool, str, dict)\n    "
    polling_increment_secs = 5
    wait_timeout = (time.time() + wait_timeout)
    status_achieved = False
    stream = dict()
    err_msg = ''
    while (wait_timeout > time.time()):
        try:
            (find_success, find_msg, stream) = find_stream(client, stream_name, check_mode=check_mode)
            if check_mode:
                status_achieved = True
                break
            elif (status != 'DELETING'):
                if (find_success and stream):
                    if (stream.get('StreamStatus') == status):
                        status_achieved = True
                        break
            elif (not find_success):
                status_achieved = True
                break
        except botocore.exceptions.ClientError as e:
            err_msg = to_native(e)
        time.sleep(polling_increment_secs)
    if (not status_achieved):
        err_msg = 'Wait time out reached, while waiting for results'
    else:
        err_msg = 'Status {0} achieved successfully'.format(status)
    return (status_achieved, err_msg, stream)
