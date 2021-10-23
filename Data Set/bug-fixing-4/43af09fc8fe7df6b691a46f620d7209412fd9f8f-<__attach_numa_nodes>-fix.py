def __attach_numa_nodes(self, entity):
    updated = False
    numa_nodes_service = self._service.service(entity.id).numa_nodes_service()
    if (len(self.param('numa_nodes')) > 0):
        existed_numa_nodes = numa_nodes_service.list()
        existed_numa_nodes.sort(reverse=((len(existed_numa_nodes) > 1) and (existed_numa_nodes[1].index > existed_numa_nodes[0].index)))
        for current_numa_node in existed_numa_nodes:
            numa_nodes_service.node_service(current_numa_node.id).remove()
            updated = True
    for numa_node in self.param('numa_nodes'):
        if ((numa_node is None) or (numa_node.get('index') is None) or (numa_node.get('cores') is None) or (numa_node.get('memory') is None)):
            continue
        numa_nodes_service.add(otypes.VirtualNumaNode(index=numa_node.get('index'), memory=numa_node.get('memory'), cpu=otypes.Cpu(cores=[otypes.Core(index=core) for core in numa_node.get('cores')]), numa_node_pins=([otypes.NumaNodePin(index=pin) for pin in numa_node.get('numa_node_pins')] if (numa_node.get('numa_node_pins') is not None) else None)))
        updated = True
    return updated