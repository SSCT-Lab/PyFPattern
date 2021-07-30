#!/usr/bin/env python3

import ast
import os
from pprint import pprint
import astunparse

from lcs import lcslen
from diffFile.reWriteName import ReWriteName

addCode = ''  # global var:fixed code
delCode = ''  # global var:buggy code

delCodeDict = {}
addCodeDict = {}

class pyCodeDiff:

    def __init__(self):
        pass

    def codeDiff(self, c, x, y, i, j, ):
        global addCode, delCode

        if i < 0 and j < 0:
            pass
            # return ""
        elif x[i] == y[j]:
            self.codeDiff(c, x, y, i - 1, j - 1)
        elif i < 0:
            self.codeDiff(c, x, y, i, j - 1)
            # addCode += "+ " + y[j]
            addCode += y[j]
        elif j < 0:
            self.codeDiff(c, x, y, i - 1, j)
            # delCode += "- " + x[i]
            delCode += x[i]
        elif c[i][j - 1] >= c[i - 1][j]:
            self.codeDiff(c, x, y, i, j - 1)
            # addCode += "+ " + y[j]
            addCode += y[j]
        elif c[i][j - 1] < c[i - 1][j]:
            self.codeDiff(c, x, y, i - 1, j)
            # delCode += "- " + x[i]
            delCode += x[i]

    def diff(self, x, y):
        c = lcslen(x, y)
        self.codeDiff(c, x, y, len(x) - 1, len(y) - 1)

def getFileList(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.py':
                L.append(os.path.join(root, file))
    return L

def readCode(code):  # AST syntax rule
    if len(code.splitlines()) == 1:
        code = code.splitlines()[0].strip()
        if code.startswith('if') or code.startswith('for') or code.startswith('with'):
            code = code + 'pass'
    else:
        tag = 0
        for index in range(0, len(code)):
            if code[index] != ' ':
                tag = index
                break
        temp = ''
        for i in code.splitlines():
            temp = temp + i[tag:] + '\n'
        code = temp.strip()
    return code

def renameCode(delCode, addCode):
    buggyCodeAST = ast.parse(delCode).body
    visitor = ReWriteName()
    for node in buggyCodeAST:
        funNode = visitor.visit(node)
        buggyCode = astunparse.unparse(funNode)

    fixedCodeAST = ast.parse(addCode).body
    for node in fixedCodeAST:
        funNode = visitor.visit(node)
        fixedCode = astunparse.unparse(funNode)

    return buggyCode, fixedCode

def getLocalVar(L):
    global addCode, delCode
    count = 0

    for i in range(0, len(L) - 1, 2):
        if L[i].endswith('bug.py'):
            buggyPath = L[i]
            fixedPath = L[i + 1]
        else:
            buggyPath = L[i + 1]
            fixedPath = L[i]

        with open(buggyPath, 'r') as f1, open(fixedPath, 'r') as f2:  # diff bug-fixing code
            try:
                codeDiff = pyCodeDiff()
                codeDiff.diff(f1.readlines(), f2.readlines())
            except Exception as e:
                continue

        if delCode == '' or delCode == '\n' or delCode == '\n\n': continue  # print(buggyPath)  # bug code is null
        if addCode == '' or addCode == '\n' or addCode == '\n\n':  continue  # print(buggyPath)  # fixed code is null

        delCode = readCode(delCode)
        addCode = readCode(addCode)

        if delCode == addCode: continue  # move bug code location

        # try:
        #     buggyCode, fixedCode = renameCode(delCode, addCode)
        #     # print('\n',buggyPath)
        #     # print(delCode)
        #     # print(addCode.strip())
        #
        #     # keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
        #     #              'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
        #     #              'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while',
        #     #              'with', 'yield','list','dict','tuple','int','str','long','bool']
        #     # featureList = ['isinstance', 'type', 'globals', 'locals', 'dir', '__dir__', 'isclass',
        #     #                 'ismethod', 'isfunction', 'getattr', '__getattribute__', 'hasattr',
        #     #                 'issubclass', 'super', 'vars', 'delattr', '__delattr__', 'setattr',
        #     #                 '__setattr__', 'property', 'reload', '__import__', 'input', 'eval',
        #     #                 'exec', 'compile', 'execfile']
        #     # for i in featureList:
        #     if (' in ' in buggyCode and 'any' not in buggyCode) and \
        #            ('any' in fixedCode and ' is ' not in fixedCode) :
        #         count = count + 1
        #         # print(buggyCode)
        #         # print(fixedCode)
        #         # print('________________________________')
        # except:
        #     pass


        if len(delCode.splitlines()) == 1 and len(addCode.splitlines()) == 1:  # len(delCode) + len(addCode) = 6
            try:
                delCodeAST = ast.parse(delCode)
                if str(delCodeAST.body[0]).startswith('<_ast.If'):  # AST type
                    count = count + 1
                    buggyCode, fixedCode = renameCode(delCode, addCode)

                    print('\n',buggyPath)
                    print(delCode)
                    print(addCode.strip())
                    print(buggyCode)
                    print(fixedCode)
                    print('________________________________')

                    if buggyCode.splitlines()[1] == "'s'": continue  # typo bugs
                    if fixedCode.splitlines()[1] == "'s'": continue

                    delCodeDict[buggyPath] = set()
                    delCodeDict[buggyPath].add(buggyCode)
                    addCodeDict[fixedPath] = set()
                    addCodeDict[fixedPath].add(fixedCode)

                # elif str(delCodeAST.body[0]).startswith('<_ast.Expr'):
                # elif str(delCodeAST.body[0]).startswith('<_ast.Return'):
                # elif str(delCodeAST.body[0]).startswith('<_ast.Raise'):
                # elif str(delCodeAST.body[0]).startswith('<_ast.Assert'):
                # elif str(delCodeAST.body[0]).startswith('<_ast.For'):
                # elif str(delCodeAST.body[0]).startswith('<_ast.If'):
                # elif str(delCodeAST.body[0]).startswith('<_ast.With'):
            except:
                # if delCode.startswith('except'):  print(len(delCode.splitlines()),len(addCode.splitlines()))
                pass

        addCode = ''
        delCode = ''
    print(count)

def compare(delCodeDict):
    from collections import defaultdict
    from collections import deque
    from apted import APTED, PerEditOperationConfig
    from apted import APTED, Config

    class Tree(object):
        """Represents a Tree Node"""

        def __init__(self, name, *children):
            self.name = name
            self.children = list(children)

        def bracket(self):
            """Show tree using brackets notation"""
            result = str(self.name)
            for child in self.children:
                result += child.bracket()
            return "{{{}}}".format(result)

        def __repr__(self):
            return self.bracket()

        @classmethod
        def from_text(cls, text):
            """Create tree from bracket notation

            Bracket notation encodes the trees with nested parentheses, for example,
            in tree {A{B{X}{Y}{F}}{C}} the root node has label A and two children
            with labels B and C. Node with label B has three children with labels
            X, Y, F.
            """
            tree_stack = []
            stack = []
            for letter in text:
                if letter == "{":
                    stack.append("")
                elif letter == "}":
                    text = stack.pop()
                    children = deque()
                    while tree_stack and tree_stack[-1][1] > len(stack):
                        child, _ = tree_stack.pop()
                        children.appendleft(child)

                    tree_stack.append((cls(text, *children), len(stack)))
                else:
                    stack[-1] += letter
            return tree_stack[0][0]

    def dedupe_nodes(l):
        new_list = []
        ids_collected = []
        for i in l:
            if i["id"] not in ids_collected:
                new_list.append(i)
                ids_collected.append(i["id"])
        return new_list

    def node_properties(node):
        d = {}
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                d[field] = node_properties(value)
            elif (
                    isinstance(value, list) and len(value) > 0 and isinstance(value[0], ast.AST)
            ):
                d[field] = [node_properties(v) for v in value]
            else:
                d[field] = value
        return d

    def node_to_dict(node, parent):
        i = []
        children = list(ast.iter_child_nodes(node))
        if len(children) > 0:
            for n in children:
                i.extend(node_to_dict(n, node))

        d = node_properties(node)
        if hasattr(node, "lineno"):
            d["lineno"] = node.lineno
        i.append(
            {
                "id": id(node),
                "name": type(node).__name__,
                "parent": id(parent),
                "data": d,
            }
        )
        return i

    def bulidTree(codeTree):

        def tree():
            return defaultdict(tree)

        def add(t, keys):
            for key in keys:
                t = t[key]

        def dicts(t):
            # return {k: dicts(t[k]) for k in t}
            dic = {}
            for k in t:
                dic[k] = dicts(t[k])
            return dic

        def TreeText(t):
            text = {}
            for k in t:
                text[k] = TreeText(t[k])

            treeTxt = str(text).replace('{}', '').replace('\'', '').replace(':', '').replace(' ', '').replace(',', '}{')
            return text

        def tagName(cur_node):
            if cur_node['name'] == 'arg':
                return cur_node['data']['arg']
            elif cur_node['name'] == 'Name':
                return cur_node['data']['id']
            elif cur_node['name'] == 'Num':
                return cur_node['data']['n']
            elif cur_node['name'] == 'Attribute':
                return cur_node['data']['attr']
            else:
                return cur_node['name']

        parent_List = []
        for i in codeTree:  # 遍历找到root id
            parent_List.append(i['parent'])
        leafNode = []
        for i in codeTree:  # 遍历找到leaf id
            if i['id'] not in parent_List:
                leafNode.append(i)

        path_List = []
        test = tree()
        for i in leafNode:
            cur_node = i
            s = str(tagName(cur_node))
            for i in codeTree:
                if cur_node['parent'] == i['id']:
                    cur_node = i
                    r = tagName(cur_node)
                    s = str(r) + ',' + s
            path_List.append(s)
            add(test, s.split(','))
        tree = dicts(test)
        # pprint(tree)
        treeTxt = TreeText(test)
        treeTxt = str(treeTxt).replace('{}', '').replace('\'', '').replace(':', '').replace(' ', '').replace(',', '}{')
        # print(treeTxt)
        return treeTxt

    resultList = set()

    for i in range(0, len(list(enumerate(delCodeDict))) - 1):
        temp = set()
        temp.add(list(delCodeDict.keys())[i])
        for j in range(i + 1, len(list(enumerate(delCodeDict)))):

            code1 = list(list(delCodeDict.values())[i])[0]
            code2 = list(list(delCodeDict.values())[j])[0]

            try:
                tree1 = ast.parse(code1)
                tree2 = ast.parse(code2)
            except:
                continue

            nodeDict1 = node_to_dict(tree1, None)
            data1 = dedupe_nodes(nodeDict1)
            text1 = bulidTree(data1)

            nodeDict2 = node_to_dict(tree2, None)
            data2 = dedupe_nodes(nodeDict2)
            text2 = bulidTree(data2)

            text1, text2 = map(Tree.from_text, [text1, text2])
            apted = APTED(text1, text2, PerEditOperationConfig(1, 1, 100))  # del_cost, ins_cost, ren_cost
            ted = apted.compute_edit_distance()

            if ted <= 5: #0，1-5
                # print(i,'~',j,ted)
                temp.add(list(delCodeDict.keys())[j])

        if len(temp) > 3:
            for i in temp:
                x = i.replace('bug.py', 'fix.py')
                s = str(list(delCodeDict[i])[0]).strip().splitlines()[0]
                    # + '    ' + \
                    # str(list(addCodeDict[x])[0]).strip().splitlines()[0]
                # s = str(i)
                resultList.add(s)
                # print(str(list(addCodeDict[x])[0]).strip())
                # print(str(list(delCodeDict[i])[0]).strip(),'\n+++++++\n',list(addCodeDict[x])[0].strip())

    pprint(len(resultList))
    # for i in resultList:
    #     print(i)

if __name__ == '__main__':
    fileList = getFileList('../dataset') # your data set path
    fileList.sort()

    getLocalVar(fileList)
    # compare(delCodeDict)










