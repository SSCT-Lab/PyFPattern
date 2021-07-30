import ast
from sys import argv

import networkx as nx

from ddg.var_ddg import MyVisitor
from graphviz import Digraph



dot = Digraph(comment='DDG')

def get_ddg(code):
    obj = MyVisitor(code)
    obj.construct_ddg()
    graphs = obj.get_function_level_ddg()
    return graphs

def render_graph(edges, method_name):
    print(edges)
    dot.edges(edges)
    # dot.save('./img/{0}.dot'.format(method_name))
    dot.render('../ddg/img/.{0}.dot'.format(method_name), view=False)

def readCode(code,method_name):
    _graph = get_ddg(code)

    # edges = list(_graph['_global_'])
    edges = sorted(_graph['_global_'], key = lambda kv:(kv[1], kv[0]))
    # render_graph(edges, method_name)

    # print(edges)
    return edges





