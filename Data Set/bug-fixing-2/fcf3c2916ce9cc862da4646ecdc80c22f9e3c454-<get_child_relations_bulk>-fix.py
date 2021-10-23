

def get_child_relations_bulk(self, instance_list):
    node_ids = []
    for i in instance_list:
        node_ids.append(i.data.id)
        i.data = None
    return [BaseRelation({
        'nodes': node_ids,
    }, NodeDeletionTask)]
