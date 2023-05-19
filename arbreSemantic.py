from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Root:
    cos: Terme

@dataclass
class Variable:
    nom: str

@dataclass
class Parentesis:
    cos: Terme

@dataclass
class Abstracio:
    lambdaSymbol: str
    parametre: Variable
    cos: Terme

@dataclass
class Aplicacio:
    funcio: Terme
    argument: Terme

Terme = Variable | Parentesis | Abstracio | Aplicacio