def get_node_inspect(self, node_id=None, skip_missing=False):
    "\n        Returns Swarm node info as in 'docker node inspect' command about single node\n\n        :param skip_missing: if True then function will return None instead of failing the task\n        :param node_id: node ID or name, if None then method will try to get node_id of host module run on\n        :return:\n            Single node information structure\n        "
    if (node_id is None):
        node_id = self.get_swarm_node_id()
    if (node_id is None):
        self.fail('Failed to get node information.')
    try:
        node_info = self.inspect_node(node_id=node_id)
    except APIError as exc:
        if (exc.status_code == 503):
            self.fail('Cannot inspect node: To inspect node execute module on Swarm Manager')
        if (exc.status_code == 404):
            if (skip_missing is False):
                self.fail(('Error while reading from Swarm manager: %s' % to_native(exc)))
            else:
                return None
    except Exception as exc:
        self.fail(('Error inspecting swarm node: %s' % exc))
    json_str = json.dumps(node_info, ensure_ascii=False)
    node_info = json.loads(json_str)
    return node_info