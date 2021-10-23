def get_child_relations_bulk(self, instance_list):
    node_ids = [i.data.id for i in instance_list]
    return [BaseRelation({
        'nodes': node_ids,
    }, NodeDeletionTask)]