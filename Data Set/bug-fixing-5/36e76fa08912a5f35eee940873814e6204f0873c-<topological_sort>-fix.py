def topological_sort(self):
    '\n        Sorts tasks in topographical order, such that a task comes after any of its\n        upstream dependencies.\n\n        Heavily inspired by:\n        http://blog.jupo.org/2012/04/06/topological-sorting-acyclic-directed-graphs/\n\n        :return: list of tasks in topological order\n        '
    graph_unsorted = OrderedDict(((task.task_id, task) for task in self.tasks))
    graph_sorted = []
    if (len(self.tasks) == 0):
        return tuple(graph_sorted)
    while graph_unsorted:
        acyclic = False
        for node in list(graph_unsorted.values()):
            for edge in node.upstream_list:
                if (edge.task_id in graph_unsorted):
                    break
            else:
                acyclic = True
                del graph_unsorted[node.task_id]
                graph_sorted.append(node)
        if (not acyclic):
            raise AirflowException('A cyclic dependency occurred in dag: {}'.format(self.dag_id))
    return tuple(graph_sorted)