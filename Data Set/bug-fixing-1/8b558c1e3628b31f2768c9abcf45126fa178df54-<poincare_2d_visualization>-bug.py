

def poincare_2d_visualization(model, tree, figure_title, num_nodes=50, show_node_labels=()):
    'Create a 2-d plot of the nodes and edges of a 2-d poincare embedding.\n\n    Parameters\n    ----------\n    model : :class:`~gensim.models.poincare.PoincareModel`\n        The model to visualize, model size must be 2.\n    tree : set\n        Set of tuples containing the direct edges present in the original dataset.\n    figure_title : str\n        Title of the plotted figure.\n    num_nodes : int or None\n        Number of nodes for which edges are to be plotted.\n        If `None`, all edges are plotted.\n        Helpful to limit this in case the data is too large to avoid a messy plot.\n    show_node_labels : iterable\n        Iterable of nodes for which to show labels by default.\n\n    Returns\n    -------\n    :class:`plotly.graph_objs.Figure`\n        Plotly figure that contains plot.\n\n    '
    vectors = model.kv.syn0
    if (vectors.shape[1] != 2):
        raise ValueError('Can only plot 2-D vectors')
    node_labels = model.kv.index2word
    nodes_x = list(vectors[:, 0])
    nodes_y = list(vectors[:, 1])
    nodes = go.Scatter(x=nodes_x, y=nodes_y, mode='markers', marker=dict(color='rgb(30, 100, 200)'), text=node_labels, textposition='bottom')
    (nodes_x, nodes_y, node_labels) = ([], [], [])
    for node in show_node_labels:
        vector = model.kv[node]
        nodes_x.append(vector[0])
        nodes_y.append(vector[1])
        node_labels.append(node)
    nodes_with_labels = go.Scatter(x=nodes_x, y=nodes_y, mode='markers+text', marker=dict(color='rgb(200, 100, 200)'), text=node_labels, textposition='bottom')
    node_out_degrees = Counter((hypernym_pair[1] for hypernym_pair in tree))
    if (num_nodes is None):
        chosen_nodes = list(node_out_degrees.keys())
    else:
        chosen_nodes = list(sorted(node_out_degrees.keys(), key=(lambda k: (- node_out_degrees[k]))))[:num_nodes]
    edges_x = []
    edges_y = []
    for (u, v) in tree:
        if (not ((u in chosen_nodes) or (v in chosen_nodes))):
            continue
        vector_u = model.kv[u]
        vector_v = model.kv[v]
        edges_x += [vector_u[0], vector_v[0], None]
        edges_y += [vector_u[1], vector_v[1], None]
    edges = go.Scatter(x=edges_x, y=edges_y, mode='line', hoverinfo=False, line=dict(color='rgb(50,50,50)', width=1))
    layout = go.Layout(title=figure_title, showlegend=False, hovermode='closest', width=800, height=800)
    return go.Figure(data=[edges, nodes, nodes_with_labels], layout=layout)
