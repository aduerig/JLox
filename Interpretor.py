from TokenType import TokenType, Token
from VisitStatement import EvaluateStatement


# Evaluates statements
class Interpretor:
    def __init__(self, lox_instance):
        self.lox_instance = lox_instance

    
    def interpret(self, statements):
        for statement in statements:
            statement.accept(EvaluateStatement)