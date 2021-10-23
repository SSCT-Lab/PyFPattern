def generate_s3_offload_dict(array):
    offload_info = {
        
    }
    api_version = array._list_available_rest_versions()
    if (S3_REQUIRED_API_VERSION in api_version):
        offload = array.list_s3_offload()
        for target in range(0, len(offload)):
            offloadt = offload[target]['name']
            offload_info[offloadt] = {
                'status': offload[target]['status'],
                'bucket': offload[target]['bucket'],
                'protocol': offload[target]['protocol'],
                'access_key_id': offload[target]['access_key_id'],
            }
    return offload_info