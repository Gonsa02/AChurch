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
        4,0,10,52,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,
        3,5,3,31,8,3,10,3,12,3,34,9,3,1,4,1,4,1,5,1,5,1,6,1,6,1,7,1,7,1,
        8,1,8,1,9,4,9,47,8,9,11,9,12,9,48,1,9,1,9,0,0,10,1,1,3,2,5,3,7,4,
        9,5,11,6,13,7,15,8,17,9,19,10,1,0,6,1,0,97,122,1,0,65,90,1,0,48,
        57,2,0,92,92,955,955,2,0,61,61,8801,8801,3,0,9,10,13,13,32,32,54,
        0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,
        1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,1,21,
        1,0,0,0,3,23,1,0,0,0,5,25,1,0,0,0,7,27,1,0,0,0,9,35,1,0,0,0,11,37,
        1,0,0,0,13,39,1,0,0,0,15,41,1,0,0,0,17,43,1,0,0,0,19,46,1,0,0,0,
        21,22,5,40,0,0,22,2,1,0,0,0,23,24,5,41,0,0,24,4,1,0,0,0,25,26,5,
        46,0,0,26,6,1,0,0,0,27,32,3,11,5,0,28,31,3,11,5,0,29,31,3,13,6,0,
        30,28,1,0,0,0,30,29,1,0,0,0,31,34,1,0,0,0,32,30,1,0,0,0,32,33,1,
        0,0,0,33,8,1,0,0,0,34,32,1,0,0,0,35,36,7,0,0,0,36,10,1,0,0,0,37,
        38,7,1,0,0,38,12,1,0,0,0,39,40,7,2,0,0,40,14,1,0,0,0,41,42,7,3,0,
        0,42,16,1,0,0,0,43,44,7,4,0,0,44,18,1,0,0,0,45,47,7,5,0,0,46,45,
        1,0,0,0,47,48,1,0,0,0,48,46,1,0,0,0,48,49,1,0,0,0,49,50,1,0,0,0,
        50,51,6,9,0,0,51,20,1,0,0,0,4,0,30,32,48,1,6,0,0
    ]

class lcLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    MACRO = 4
    LLETRA = 5
    LLETRAMAJUSCULA = 6
    DIGIT = 7
    LAMBDA = 8
    ASSIGNACIO = 9
    WS = 10

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "'.'" ]

    symbolicNames = [ "<INVALID>",
            "MACRO", "LLETRA", "LLETRAMAJUSCULA", "DIGIT", "LAMBDA", "ASSIGNACIO", 
            "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "MACRO", "LLETRA", "LLETRAMAJUSCULA", 
                  "DIGIT", "LAMBDA", "ASSIGNACIO", "WS" ]

    grammarFileName = "lc.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


