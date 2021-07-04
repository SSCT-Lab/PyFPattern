import ast
from pprint import pprint
import astunparse

from pyff.diffFile.reWriteName import ReWriteName

def pattern_C1(delCode, generatedPatch, candidateObj):
    left = delCode.split('=')[0].strip()
    right = delCode.split('=')[1].strip()

    # C1.1
    fixedCode = left + ' = ' + 'str(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'bool(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'int(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'bytes(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'float(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'tuple(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'list(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'set(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'frozenset(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'dict(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'chr(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'ord(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'hex(' + right + ')'
    generatedPatch.add(fixedCode)
    fixedCode = left + ' = ' + 'oct(' + right + ')'
    generatedPatch.add(fixedCode)

    # C1.2 & C1.3
    for i in candidateObj:
        fixedCode = left + ' = ' + i
        generatedPatch.add(fixedCode)

    buggyCodeAST = ast.parse(right).body
    visitor = ReWriteName(candidateObj)
    for node in buggyCodeAST:
        buggyObj = visitor.visit(node)

    for i in candidateObj:
        for j in buggyObj:
            fixedCode = left + ' = ' + right.replace(j, i)
            generatedPatch.add(fixedCode)

    return generatedPatch

def pattern_C2(delCode, generatedPatch, candidateObj):


    # C 2.1
    buggyCodeAST = ast.parse(delCode).body
    visitor = ReWriteName()
    for node in buggyCodeAST:
        buggyObj = visitor.visit(node)

    buggyObj = list(buggyObj)
    for i in candidateObj:
        for j in buggyObj:
            fixedCode = delCode.replace(j, i)
            generatedPatch.add(fixedCode)

    # C 2.2 & 2.3
    argList = []
    start_index = delCode.find('(')
    end_index = delCode.find(')')
    if ',' in delCode[start_index:end_index]:
        temp = str(delCode[start_index:end_index]).replace('(','').replace(')','')
        argList = argList+temp.split(',')


    for i in range(0,len(argList)):
        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[i].strip()))
        generatedPatch.add(fixedCode)

    if len(argList) == 2:
        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[1].strip()+','+argList[0].strip()))
        generatedPatch.add(fixedCode)

    if len(argList) == 3:
        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[0].strip()+','+argList[1].strip()))
        generatedPatch.add(fixedCode)
        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[1].strip()+','+argList[0].strip()))
        generatedPatch.add(fixedCode)
        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[1].strip()+','+argList[2].strip()))
        generatedPatch.add(fixedCode)
        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[2].strip()+','+argList[1].strip()))
        generatedPatch.add(fixedCode)
        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[0].strip()+','+argList[2].strip()))
        generatedPatch.add(fixedCode)
        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[2].strip()+','+argList[0].strip()))
        generatedPatch.add(fixedCode)

        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[0].strip()+','+argList[2].strip()+','+argList[1].strip()))
        generatedPatch.add(fixedCode)
        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[1].strip()+','+argList[0].strip()+','+argList[2].strip()))
        generatedPatch.add(fixedCode)
        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[1].strip()+','+argList[2].strip()+','+argList[0].strip()))
        generatedPatch.add(fixedCode)
        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[2].strip()+','+argList[0].strip()+','+argList[1].strip()))
        generatedPatch.add(fixedCode)
        fixedCode = delCode.replace(delCode[start_index:end_index],str('('+argList[2].strip()+','+argList[1].strip()+','+argList[0].strip()))
        generatedPatch.add(fixedCode)

    return generatedPatch

def pattern_C3(delCode, generatedPatch, candidateObj):
    optList = ['>','<','>=','<=','>>','<<','!=',]
    print(delCode)

    for i in optList:
        if i in delCode:
            tag = delCode.find(i)
    for i in optList:
        fixedCode = delCode.replace(delCode[tag],i)
        generatedPatch.add(fixedCode)

    for i in optList:
        if i in delCode:
            for j in candidateObj:
                # changed condition  ...
                fixedCode = delCode.replace(delCode.split(i)[0].split(' ')[1],' '+j)
                generatedPatch.add(fixedCode)

                fixedCode = delCode.replace(delCode.split(i)[1],' '+j)
                generatedPatch.add(fixedCode)

                # remove condition ...
                fixedCode = 'if '+ delCode.split(i)[0].split(' ')[1] + ': pass'
                generatedPatch.add(fixedCode)
                fixedCode = 'if '+ delCode.split(i)[1] + ': pass'
                generatedPatch.add(fixedCode)

    return generatedPatch

def pattern_C4(delCode, generatedPatch, candidateObj):

    if '.keys()' in delCode:
        fixedCode = delCode.replace('in','in list (')
        fixedCode = delCode.replace(')','))')
        generatedPatch.add(fixedCode)

    return generatedPatch

def pattern_C5(delCode, generatedPatch, candidateObj):
    argList = ['r','w','a','rb','wb','ab','w+','a+','rb+','wb+','ab+']

    delCode = 'with open(local_file,’r’) as f: pass'

    if 'open(' in delCode:
        for i in argList:
            if i in delCode:
                start_index = delCode.find(',')
                end_index = delCode.find(')')
                temp = delCode[start_index+1:end_index]
                break

    for i in argList:
        fixedCode = delCode.replace(temp,'\''+i+'\'')
        generatedPatch.add(fixedCode)

    return generatedPatch

def fix_pattern(delCode, addCode, ddg_graph, buggyPath):
    generatedPatch = set()
    candidateObj = set()
    for (key) in ddg_graph.keys():
        candidateObj.add(key)
        for key, value in ddg_graph[key].items():
            candidateObj.add(key)
            for i in value:
                candidateObj.add(i)

    try:
        buggyCodeAST = ast.parse(delCode)

        if str(buggyCodeAST.body[0]).startswith('<_ast.Assign'):
            generatedPatch = pattern_C1(delCode, generatedPatch, candidateObj)
            pprint(generatedPatch)

        if str(buggyCodeAST.body[0]).startswith('<_ast.Expr'):
            generatedPatch = pattern_C2(delCode, generatedPatch, candidateObj)
            pprint(generatedPatch)

        if str(buggyCodeAST.body[0]).startswith('<_ast.If'):
            generatedPatch = pattern_C3(delCode, generatedPatch, candidateObj)
            pprint(generatedPatch)

        if str(buggyCodeAST.body[0]).startswith('<_ast.For'):
            generatedPatch = pattern_C4(delCode, generatedPatch, candidateObj)
            pprint(generatedPatch)

        if str(buggyCodeAST.body[0]).startswith('<_ast.Raise'):
            print(buggyCodeAST.body)

        if str(buggyCodeAST.body[0]).startswith('<_ast.With'):
            generatedPatch = pattern_C5(delCode, generatedPatch, candidateObj)
            pprint(generatedPatch)


    except:
        # if delCode.startswith('except'): pass
        pass

class ReWriteName(ast.NodeTransformer, ):
    def __init__(self):
        self.defList = []
        self.varList = []
        self.argList = []
        self.funList = []
        self.numList = []
        self.strList = []
        self.moduleList = []
        self.keywords = ['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
                         'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
                         'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while',
                         'with', 'yield']
        self.featureList = ['isinstance', 'type', 'globals', 'locals', 'dir', '__dir__', 'isclass',
                            'ismethod', 'isfunction', 'getattr', '__getattribute__', 'hasattr',
                            'issubclass', 'super', 'vars', 'delattr', '__delattr__', 'setattr',
                            '__setattr__', 'property', 'reload', '__import__', 'input', 'eval',
                            'exec', 'compile', 'execfile']
        self.obj = []

    def generic_visit(self, node):

        if hasattr(node, 'module'):
            self.obj.append(node.module)

        if hasattr(node, 'name'):
            self.obj.append(node.name)

        if hasattr(node, 'arg'):
            self.obj.append(node.arg)

        if hasattr(node, 'id'):
            if (node.id in self.keywords) or (node.id in self.featureList):
                node.id = node.id
            else:
                self.obj.append(node.id)

        if hasattr(node, 'attr'):
            if (node.attr in self.keywords) or (node.attr in self.featureList):
                node.attr = node.attr
            else:
                self.obj.append(node.attr)

        ast.NodeTransformer.generic_visit(self, node)

        return self.obj
