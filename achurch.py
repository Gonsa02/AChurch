from __future__ import annotations
from dataclasses import dataclass
from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser
from lcVisitor import lcVisitor


@dataclass
class Root:
    cos: Terme


@dataclass
class Variable:
    nom: str


@dataclass
class Abstracio:
    lambdaSymbol: str
    parametre: Variable
    cos: Terme


@dataclass
class Aplicacio:
    funcio: Terme
    argument: Terme


Terme = Variable | Abstracio | Aplicacio


def parenthesize(node):
    if isinstance(node, Root):
        return f"{parenthesize(node.cos)}"
    elif isinstance(node, Variable):
        return node.nom
    elif isinstance(node, Abstracio):
        return f"({node.lambdaSymbol}{parenthesize(node.parametre)}.{parenthesize(node.cos)})"
    elif isinstance(node, Aplicacio):
        return f"({parenthesize(node.funcio)}{parenthesize(node.argument)})"
    else:
        raise ValueError("Node invàlid")

"""
    Substitution rep el node a partir del cual es farà la substitució, el parametre es el valor
    a substituir i el valor es pel node que es substituirà
"""
def substitution(node, parametre, valor):
    if isinstance(node, Variable):
        if node.nom == parametre.nom:
            return valor 
        else:
            return node
    elif isinstance(node, Abstracio):
        return Abstracio(node.lambdaSymbol, node.parametre, substitution(node.cos, parametre, valor))
    elif isinstance(node, Aplicacio):
        return Aplicacio(substitution(node.funcio, parametre, valor), substitution(node.argument, parametre, valor))
    else:
        raise ValueError("Node invàlid")


def betaReduction(node):
    if isinstance(node, Aplicacio) and isinstance(node.funcio, Abstracio):
        return substitution(node.funcio.cos, node.funcio.parametre, node.argument)
    elif isinstance(node, Aplicacio):
        return Aplicacio(betaReduction(node.funcio), betaReduction(node.argument))
    elif isinstance(node, Variable):
        return node
    elif isinstance(node, Root):
        return Root(betaReduction(node.cos))
    else:
        raise ValueError("Node invalid, ha de ser una aplicació i una abstraccio per fer una β-reducció \
                         i es " + str(type(node)) + " " + str(type(node.funcio)))

def checkBetaReduction(node):
    if isinstance(node, Aplicacio) and isinstance(node.funcio, Abstracio):
        return node
    elif isinstance(node, Aplicacio):
        if checkBetaReduction(node.funcio) == None:
            return checkBetaReduction(node.argument)
        else:
            return checkBetaReduction(node.funcio)
    elif isinstance(node, Variable):
        return None
    elif isinstance(node, Root):
        return checkBetaReduction(node.cos)

def redueix(node, limit):
    if isinstance(node, Root):
        while limit > 0:
            node_aux = checkBetaReduction(node)
            if node_aux != None:
                node_aux = betaReduction(node_aux)
                print("β-reducció:")
                print(parenthesize(node) + " → " + parenthesize(node_aux))
                node = node_aux
            limit -= 1
        print("Resultat:")
        print(parenthesize(node))
    else:
        raise ValueError("Node invàlid")

class PrintVisitor(lcVisitor):

    def __init__(self):
        self.nivell = 0

    def visitRoot(self, ctx):
        [terme] = list(ctx.getChildren())
        print('  ' *  self.nivell + "R")
        self.nivell += 1
        self.visit(terme)
        self.nivell -= 1

    def visitAplicacio(self, ctx):
        [terme1, terme2] = list(ctx.getChildren())
        print('  ' *  self.nivell + "@")
        self.nivell += 1
        self.visit(terme1)
        self.visit(terme2)
        self.nivell -= 1

    def visitParentesis(self, ctx):
        [_, terme, _] = list(ctx.getChildren())
        self.visit(terme)
    
    def visitAbstraccio(self, ctx):
        [lambdaSymbol, lletra, _, terme] = list(ctx.getChildren())
        print('  ' *  self.nivell + lambdaSymbol.getText())
        self.nivell += 1
        print('  ' *  self.nivell + lletra.getText())
        self.visit(terme)
        self.nivell -= 1

    def visitVariable(self, ctx):
        [variable] = list(ctx.getChildren())
        print('  ' *  self.nivell + variable.getText())


class TreeVisitor(lcVisitor):

    def visitRoot(self, ctx):
        [terme] = list(ctx.getChildren())
        res = self.visit(terme)
        return Root(res)

    def visitParentesis(self, ctx):
        [_, terme, _] = list(ctx.getChildren())
        return self.visit(terme)

    def visitVariable(self, ctx):
        [lletra] = list(ctx.getChildren())
        return Variable(lletra.getText())

    def visitAbstraccio(self, ctx):
        [lambdaSymbol, lletra, _, terme] = list(ctx.getChildren())
        res = self.visit(terme)
        return Abstracio(lambdaSymbol.getText(), Variable(lletra.getText()), res)

    def visitAplicacio(self, ctx):
        [terme1, terme2] = list(ctx.getChildren())
        res1 = self.visit(terme1)
        res2 = self.visit(terme2)
        return Aplicacio(res1, res2)


input_stream = InputStream(input('? '))
lexer = lcLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = lcParser(token_stream)
tree = parser.root()
if parser.getNumberOfSyntaxErrors() == 0:
    visitor = TreeVisitor()
    printvisitor = PrintVisitor()
    #print(tree.toStringTree(recog=parser))
    printvisitor.visit(tree)
    arbreSemantic = visitor.visit(tree)
    print("Arbre:")
    print(parenthesize(arbreSemantic))
    redueix(arbreSemantic, 10)
else: 
    print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
    print(tree.toStringTree(recog=parser))

"""
input_stream = InputStream(input('? '))
while input_stream:
    lexer = lambdaCalculLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = lambdaCalculParser(token_stream)
    tree = parser.root()
    if parser.getNumberOfSyntaxErrors() == 0:
        print("OKEY")
    else: 
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser))
"""