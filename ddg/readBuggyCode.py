import ast
import re
from filecmp import cmp
from pprint import pprint
import os
import astunparse

from ddg import getDDG


class varChain:

    def __init__(self, bugVar,ddg_graph,code_decls,codePath):

        self.bugVar = bugVar
        self.ddg_graph = ddg_graph
        self.code_decls = code_decls
        self.codePath = codePath
        self.bugDataChain = {}

        for func in self.bugVar:
            self.localBugDataChain = set()
            self.localGraphChain(self.bugVar[func], self.ddg_graph[func])
            self.bugDataChain[func] = self.localBugDataChain

        self.code = self.refactorCode()

    def localGraphChain(self,bugVar,ddgGraph):
        for var in bugVar:
            if ddgGraph.__contains__(var):
                self.localBugDataChain.add(var)
                subVar = ddgGraph[var]

                for j in subVar:
                    if (j != var) and (j in ddgGraph) and (var not in subVar):
                        self.localGraphChain(subVar, ddgGraph)

    def refactorCode(self):
        refactor_code = ''
        codeIndex = {}
        for funcName in self.bugDataChain:
            # print('funcName: ',funcName)
            indexSet = self.code_decls[funcName]
            # print(indexSet)
            varSet = self.bugDataChain[funcName]
            # print(varSet)
            temp = []
            for var in varSet:
                if var in indexSet:
                    temp.append(indexSet[var])
            temp = list(set(temp))
            temp.sort()

            codeIndex[funcName] = temp
        # print("codeIndex:",codeIndex)

        for i in codeIndex:
            if len(codeIndex[i]) !=0:

                code = open(self.codePath).read()
                body = ast.parse(code)
                _, statements = next(ast.iter_fields(body))
                refactor_CodeAST = []

                for astIndex, node in enumerate(statements):
                    if isinstance(node,ast.FunctionDef): # local method
                        for index in codeIndex[node.name]:
                            refactor_CodeAST.append(node.body[index])

                    refactor_code = str(astunparse.unparse(refactor_CodeAST).strip())

        # print(refactor_code)
        return refactor_code

def parseBuggyCode(bugPath):
    bugVar = set()
    bug_decls, bug_graph = getDDG.test(bugPath)

    for var in bug_graph:
        bugVar.add(var)
        for i in bug_graph[var]:
            bugVar.add(i)
    return bugVar

def parseBuggyFile(codePath):
    _local_code_decls, _local_graph = getDDG.test_recursive(codePath)
    return _local_code_decls, _local_graph

