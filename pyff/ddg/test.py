import networkx as nx
from ortools.sat.python import cp_model
from itertools import combinations
def var_from_domain(model, name, domain):
    "initialize a variable with integer domain defined by domain"
    domain = cp_model.Domain.FromIntervals([[i] for i in domain])
    val = model.NewIntVarFromDomain(domain, name)
    return val

def compareGraph(Graph1,Graph2):

    # G=nx.Graph([('code', 'filename'), ('code2', 'funcdict'), ('code1', 'funcdict'), ('code2', 'make_arrays'), ('code3', 'make_ufuncs'), ('code1', 'make_arrays'), ('code3', 'funcdict')])
    G=nx.Graph(Graph1)
    mapping = dict(zip(G.nodes(),range(G.number_of_nodes())))
    G = nx.relabel_nodes(G,mapping)
    # print(nx.edges(G))

    S=nx.Graph([('logits', 'pool2'), ('loss', 'target'), ('logits', 'tf'), ('loss', 'tf'), ('target', 'tf')])
    # S=nx.Graph(Graph2)
    mapping = dict(zip(S.nodes(),range(S.number_of_nodes())))
    S = nx.relabel_nodes(S,mapping)
    # print(nx.edges(S))

    model = cp_model.CpModel()

    D = list(G.nodes)
    X = {i:var_from_domain(model, "X("+str(i)+")", D) for i in S.nodes}

    # 约束：存在嵌入 S -> subgraph of G
    model.AddAllDifferent([X[i] for i in S.nodes])
    E_G = list(G.edges) + [e[::-1] for e in G.edges]
    for v1, v2 in combinations(S.nodes,2):
        if (v1,v2) in S.edges:
            model.AddAllowedAssignments((X[v1],X[v2]), E_G)
        else:
            model.AddForbiddenAssignments((X[v1],X[v2]), E_G)

    solver = cp_model.CpSolver()

    result = ''
    if len(S.nodes)==len(G.nodes):
        status = solver.Solve(model)

        if status == cp_model.FEASIBLE:
            result = '同构'
            # print("同构，嵌入为:")
            # for v, x in X.items():
            #     print('f(%s)=%i' % (v, solver.Value(x)))
        elif status == cp_model.OPTIMAL:
            result = '同样'
            # print('同样')
    #     else:
    #         pass
    #         # print("不同构")
    # else:
    #     pass
    #     # print("不同构")

    return result
