def maybe_instance_from_label(module, client):
    'Try to retrieve an instance based on a label.'
    try:
        label = module.params['label']
        result = client.linode.instances((Instance.label == label))
        return result[0]
    except IndexError:
        return None
    except Exception as exception:
        raise module.fail_json(msg=('Unable to query the Linode API. Saw: %s' % exception))