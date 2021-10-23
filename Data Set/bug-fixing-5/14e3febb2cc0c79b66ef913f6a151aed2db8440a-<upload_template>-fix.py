def upload_template(module, proxmox, api_host, node, storage, content_type, realpath, timeout):
    taskid = proxmox.nodes(node).storage(storage).upload.post(content=content_type, filename=open(realpath, 'rb'))
    while timeout:
        task_status = proxmox.nodes(api_host.split('.')[0]).tasks(taskid).status.get()
        if ((task_status['status'] == 'stopped') and (task_status['exitstatus'] == 'OK')):
            return True
        timeout = (timeout - 1)
        if (timeout == 0):
            module.fail_json(msg=('Reached timeout while waiting for uploading template. Last line in task before timeout: %s' % proxmox.node(node).tasks(taskid).log.get()[:1]))
        time.sleep(1)
    return False