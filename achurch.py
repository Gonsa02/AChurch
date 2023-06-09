from __future__ import annotations
from dataclasses import dataclass
from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser
from lcVisitor import lcVisitor


taula_macros = {}


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


def currificar(lambdaSymbol, variables, cos):
    if len(variables) == 1:
        return Abstracio(lambdaSymbol.getText(), Variable(variables[0].getText()), cos)
    else:
        return Abstracio(lambdaSymbol.getText(), Variable(variables[0].getText()), currificar(lambdaSymbol, variables[1:], cos))


def parenthesize(node):
    if isinstance(node, Variable):
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
        return Abstracio(node.lambdaSymbol, substitution(node.parametre, parametre, valor), substitution(node.cos, parametre, valor))
    elif isinstance(node, Aplicacio):
        return Aplicacio(substitution(node.funcio, parametre, valor), substitution(node.argument, parametre, valor))
    else:
        raise ValueError("Node invàlid")


def betaReduction(node):
    if isinstance(node, Aplicacio) and isinstance(node.funcio, Abstracio):
        return substitution(node.funcio.cos, node.funcio.parametre, node.argument)
    elif isinstance(node, Aplicacio):
        return Aplicacio(betaReduction(node.funcio), betaReduction(node.argument))
    elif isinstance(node, Abstracio):
        return Abstracio(node.lambdaSymbol, node.parametre, betaReduction(node.cos))
    elif isinstance(node, Variable):
        return node
    else:
        raise ValueError("Node invàlid")


"""Retorna el node Aplicacio a partir del cual podem fer una β-reducció en cas que es pugui fer,
   en cas contrari dona None.
"""
def checkBetaReduction(node):
    if isinstance(node, Aplicacio) and isinstance(node.funcio, Abstracio):
        return node
    elif isinstance(node, Aplicacio):
        aux = checkBetaReduction(node.funcio)
        if aux == None: 
            return checkBetaReduction(node.argument)
        else: 
            return aux
    elif isinstance(node, Abstracio): #Afegit rapidament, revisar si es correcte
        return checkBetaReduction(node.cos)
    else:
        return None       


"""
    Retorna una conjunt que conté tots els noms de les variables que hi ha a l'abre o subarbre que té com a arrel
    el node que es passa per paràmetre

"""
def conjuntNoms(node):
    l = set()
    if isinstance(node, Variable):
        l.add(node.nom)
    elif isinstance(node, Aplicacio):
        l = l.union(conjuntNoms(node.funcio))
        l = l.union(conjuntNoms(node.argument))
    elif isinstance(node, Abstracio):
        l = l.union(conjuntNoms(node.parametre))
        l = l.union(conjuntNoms(node.cos))
    else:
        raise ValueError("Node invàlid")
    return l


"""
    Retorna una conjunt que conté tots els noms de les variables lligades que hi ha a l'abre o subarbre que té com a arrel
    el node que es passa per paràmetre

"""
def variablesLligades(node):
    l = set()
    if isinstance(node, Abstracio):
        l.add(node.parametre.nom)
        l = l.union(variablesLligades(node.cos))
    elif isinstance(node, Aplicacio):
        l = l.union(variablesLligades(node.funcio))
        l = l.union(variablesLligades(node.argument))
    elif isinstance(node, Variable):
        return l
    else:
        raise ValueError("Node invàlid")
    return l


"""
   Aquesta funcio retorna per ordre alfabetic una lletra que no tingui conflicte amb el conjunt
   que es passa per parametre. 
"""
def novaLletra(conflicte):
    lletres_alfabet = "abcdefghijklmnopqrstuvwxyz"

    for lletra in lletres_alfabet:
        if lletra not in conflicte:
            return lletra

    return None

"""
def buscarConflicte(node):
    if isinstance(node, Aplicacio) and isinstance(node.funcio, Abstracio) and isinstance(node.funcio.cos, Abstracio):
        dreta = conjuntNoms(node.argument)
        esquerra = conjuntNoms(node.funcio.cos)
        return dreta.intersection(esquerra)
    return set()
"""

def buscarConflicte(node):
    if isinstance(node, Aplicacio):
        dreta = conjuntNoms(node.argument)
        esquerra = variablesLligades(node.funcio)
        return esquerra.intersection(dreta)
    return set()

def alphaReduction(node, conflicte):
    lletres_utilitzades = conjuntNoms(node.funcio)
    lletres_utilitzades.add(conflicte)
    nova_lletra = novaLletra(lletres_utilitzades)
    nou_node = Variable(nova_lletra)
    print("α-conversió: " + conflicte + " → " + nova_lletra)
    return Aplicacio(substitution(node.funcio, Variable(conflicte), nou_node), node.argument)   


def redueix(node, limit):
    final = False
    while not final and limit > 0:
        #Comprobem si podem fer alpha conversió, en cas que si la fem.
        conflicte = buscarConflicte(node)
        if len(conflicte) > 0:
            for i in conflicte:
                node_aux = alphaReduction(node, i)
                print(parenthesize(node.funcio) + " → " + parenthesize(node_aux.funcio))
                node = node_aux

        #Comprobem si podem fer beta reducció, en cas que si la fem.
        node_aux = checkBetaReduction(node)
        
        if node_aux != None:
            node_reduction = betaReduction(node_aux)
            print("β-reducció:")
            print(parenthesize(node_aux) + " → " + parenthesize(node_reduction))
            node = betaReduction(node)
        else:
            final = True
        limit -= 1
        if limit == 0:
            print("...")
    print("Resultat: ")
    if final:
        print(parenthesize(node))
    else:
        print("Nothing")


class TreeVisitor(lcVisitor):

    def visitParentesis(self, ctx):
        [_, terme, _] = list(ctx.getChildren())
        return self.visit(terme)

    def visitVariable(self, ctx):
        [lletra] = list(ctx.getChildren())
        return Variable(lletra.getText())

    def visitAbstraccio(self, ctx):
        lambdaSymbol, terme = list(ctx.getChildren())[0], list(ctx.getChildren())[-1]
        lletres = list(ctx.LLETRA())
        res = self.visit(terme)
        return currificar(lambdaSymbol, lletres, res)

    def visitAplicacio(self, ctx):
        [terme1, terme2] = list(ctx.getChildren())
        res1 = self.visit(terme1)
        res2 = self.visit(terme2)
        return Aplicacio(res1, res2)
    
    def visitMacro(self, ctx):
        [macro] = list(ctx.getChildren())
        expressio = taula_macros[macro.getText()]
        return expressio
    
    def visitInfix(self, ctx):
        [t1, infix, t2] = list(ctx.getChildren())
        res1 = self.visit(t1)
        res2 = self.visit(t2)
        res_infix = taula_macros[infix.getText()]
        return Aplicacio(Aplicacio(res_infix,res1), res2)
    
    def visitAssignacio(self, ctx):
        [nomMacro, _, terme] = list(ctx.getChildren())
        taula_macros[nomMacro.getText()] = self.visit(terme)
        return None
    
        

"""
input_stream = InputStream(input('? '))
while input_stream:
    lexer = lcLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = lcParser(token_stream)
    tree = parser.root()
    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = TreeVisitor()
        arbreSemantic = visitor.visit(tree)
        if arbreSemantic == None:
            for clau, valor in taula_macros.items():
                print(clau + " ≡ " + parenthesize(valor))
        else:
            print("Arbre:")
            print(parenthesize(arbreSemantic))
            redueix(arbreSemantic, 10)
    else: 
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser))
    input_stream = InputStream(input('? '))
"""
"""
class PrintVisitor(lcVisitor):

    def __init__(self):
        self.nivell = 0

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
"""

import logging
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.first_name
    await context.bot.send_message(chat_id=update.effective_chat.id, text="AChurchBot!\nBenvolgut "+ username + "!")


async def author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="@ Marc Gonzalez Vidal, 2023")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/start\n/help\n/author\n/macros")


async def macros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Macros")


async def evaluator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lexer = lcLexer(InputStream(update.message.text))
    token_stream = CommonTokenStream(lexer)
    parser = lcParser(token_stream)
    tree = parser.root()
    missatge = ""
    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = TreeVisitor()
        arbreSemantic = visitor.visit(tree)
        if arbreSemantic == None:
            missatge = "MACROS"
            for clau, valor in taula_macros.items():
                missatge += "\n"+ str(clau) + " ≡ " + parenthesize(valor)
        else:
            missatge = "Arbre:\n"+parenthesize(arbreSemantic)
            redueix(arbreSemantic, 10)
    else: 
        missatge = str(parser.getNumberOfSyntaxErrors()) + "errors de sintaxi.\n" + str(tree.toStringTree(recog=parser))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=missatge)

if __name__ == '__main__':
    TOKEN = "6111049756:AAEDkKcpj-f-wa8tmb9wE8ix-X7xLW11k6s"

    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    author_handler = CommandHandler('author', author)
    help_handler = CommandHandler('help', help)
    macros_handler = CommandHandler('macros', macros)
    evaluator_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), evaluator)
    application.add_handler(start_handler)
    application.add_handler(author_handler)
    application.add_handler(help_handler)
    application.add_handler(macros_handler)
    application.add_handler(evaluator_handler)


    
    application.run_polling()