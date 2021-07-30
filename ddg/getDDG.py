import ddg.code_to_data_dependency_graph as code2ddg
from .var_ddg import MyVisitor


def test(path):

    if path.startswith('.'):
        code = open(path).read()
        decls, graph = code2ddg.get_deps(code)
    else:
        decls, graph = code2ddg.get_deps(path)
    # print("var: line_number map =>")
    # print(decls)
    # print("variable data dependence =>")
    # print(graph)
    # for i in graph:
    #     print(i,"--->",graph[i])
    return decls, graph

def test_recursive(path):
    code = open(path).read()
    decls, graph = code2ddg.fn_ddgs(code)

    # print("variable data dependence by method name =>")
    # print("var: line_number map =>")
    # print(decls)
    # print("variable data dependence by method name =>")
    # print(graph)
    # for i in graph:
    #     print(i,"--->",graph[i])
    return decls, graph

def test_my_visitor(path):
    code = open(path).read()
    # print(code)
    obj = MyVisitor(path)
    obj.construct_ddg()
    graphs = obj.get_function_level_ddg()
    #
    # print("variable data dependence by method name =>")
    # print(graphs)
    return graphs
