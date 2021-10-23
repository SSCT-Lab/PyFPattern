def topological_sort(self):
    '\n        Sorts tasks in topographical order, such that a task comes after any of its\n        upstream dependencies.\n\n        Heavily inspired by:\n        http://blog.jupo.org/2012/04/06/topological-sorting-acyclic-directed-graphs/\n\n        :return: list of tasks in topological order\n        '
    graph_unsorted = self.tasks[:]
    graph_sorted = []
    if (len(self.tasks) == 0):
        return tuple(graph_sorted)
    while graph_unsorted:
        acyclic = False
        for node in list(graph_unsorted):
            for edge in node.upstream_list:
                if (edge in graph_unsorted):
                    break
            else:
                acyclic = True
                graph_unsorted.remove(node)
                graph_sorted.append(node)
        if (not acyclic):
            raise AirflowException('A cyclic dependency occurred in dag: {}'.format(self.dag_id))
    return tuple(graph_sorted)