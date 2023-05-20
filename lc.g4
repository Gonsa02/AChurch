grammar lc;

root : terme;

terme : terme terme                       #aplicacio
      | '(' terme ')'                     #parentesis
      | LAMBDA LLETRA+ '.' terme          #abstraccio
      | LLETRA                            #variable
      ;

LLETRA : [a-z];

LAMBDA : '\\' | 'λ';

WS : [ \t\r\n]+ -> skip;