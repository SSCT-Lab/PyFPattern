def draw_graph(startup_program, main_program, **kwargs):
    if ('graph_attr' in kwargs):
        GRAPH_STYLE.update(kwargs[graph_attr])
    if ('node_attr' in kwargs):
        OP_STYLE.update(kwargs[node_attr])
    if ('edge_attr' in kwargs):
        VAR_STYLE.update(kwargs[edge_attr])
    graph_id = unique_id()
    filename = kwargs.get('filename')
    if (filename == None):
        filename = (str(graph_id) + '.gv')
    g = Digraph(name=str(graph_id), filename=filename, graph_attr=GRAPH_STYLE, node_attr=OP_STYLE, edge_attr=VAR_STYLE, **kwargs)
    var_dict = {
        
    }
    parse_graph(startup_program, g, var_dict)
    parse_graph(main_program, g, var_dict)
    if (filename != None):
        g.save()
    return g