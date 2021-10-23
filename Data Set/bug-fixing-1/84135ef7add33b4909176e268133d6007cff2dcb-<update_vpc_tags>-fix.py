

def update_vpc_tags(vpc, module, vpc_obj, tags, name):
    if (tags is None):
        tags = dict()
    tags.update({
        'Name': name,
    })
    try:
        current_tags = dict(((t.name, t.value) for t in vpc.get_all_tags(filters={
            'resource-id': vpc_obj.id,
        })))
        if (tags != current_tags):
            if (not module.check_mode):
                vpc.create_tags(vpc_obj.id, tags)
            return True
        else:
            return False
    except Exception as e:
        e_msg = boto_exception(e)
        module.fail_json(msg=e_msg)
