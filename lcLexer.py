# Generated from lc.g4 by ANTLR 4.13.0
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,11,56,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,1,0,1,0,1,1,1,1,1,2,1,2,
        1,3,1,3,1,3,5,3,33,8,3,10,3,12,3,36,9,3,1,4,1,4,1,5,1,5,1,6,1,6,
        1,7,1,7,1,8,1,8,1,9,1,9,1,10,4,10,51,8,10,11,10,12,10,52,1,10,1,
        10,0,0,11,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,1,
        0,7,9,0,35,38,42,43,45,47,58,58,60,60,62,64,94,95,124,124,126,126,
        1,0,97,122,1,0,65,90,1,0,48,57,2,0,92,92,955,955,2,0,61,61,8801,
        8801,3,0,9,10,13,13,32,32,58,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,
        0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,
        17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,1,23,1,0,0,0,3,25,1,0,0,0,5,
        27,1,0,0,0,7,29,1,0,0,0,9,37,1,0,0,0,11,39,1,0,0,0,13,41,1,0,0,0,
        15,43,1,0,0,0,17,45,1,0,0,0,19,47,1,0,0,0,21,50,1,0,0,0,23,24,5,
        40,0,0,24,2,1,0,0,0,25,26,5,41,0,0,26,4,1,0,0,0,27,28,5,46,0,0,28,
        6,1,0,0,0,29,34,3,13,6,0,30,33,3,13,6,0,31,33,3,15,7,0,32,30,1,0,
        0,0,32,31,1,0,0,0,33,36,1,0,0,0,34,32,1,0,0,0,34,35,1,0,0,0,35,8,
        1,0,0,0,36,34,1,0,0,0,37,38,7,0,0,0,38,10,1,0,0,0,39,40,7,1,0,0,
        40,12,1,0,0,0,41,42,7,2,0,0,42,14,1,0,0,0,43,44,7,3,0,0,44,16,1,
        0,0,0,45,46,7,4,0,0,46,18,1,0,0,0,47,48,7,5,0,0,48,20,1,0,0,0,49,
        51,7,6,0,0,50,49,1,0,0,0,51,52,1,0,0,0,52,50,1,0,0,0,52,53,1,0,0,
        0,53,54,1,0,0,0,54,55,6,10,0,0,55,22,1,0,0,0,4,0,32,34,52,1,6,0,
        0
    ]

class lcLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    MACRO = 4
    INFIX = 5
    LLETRA = 6
    LLETRAMAJUSCULA = 7
    DIGIT = 8
    LAMBDA = 9
    ASSIGNACIO = 10
    WS = 11

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "'.'" ]

    symbolicNames = [ "<INVALID>",
            "MACRO", "INFIX", "LLETRA", "LLETRAMAJUSCULA", "DIGIT", "LAMBDA", 
            "ASSIGNACIO", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "MACRO", "INFIX", "LLETRA", "LLETRAMAJUSCULA", 
                  "DIGIT", "LAMBDA", "ASSIGNACIO", "WS" ]

    grammarFileName = "lc.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


