from TokenType import TokenType, Token
from VisitStatement import EvaluateStatement


# Evaluates statements
class Interpretor:
    def __init__(self, lox_instance):
        self.lox_instance = lox_instance
        self.data = {}

    
    def interpret(self, statements):
        for statement in statements:
            statement.accept(EvaluateStatement)

    
    def define(self, name, value):
        self.data[name] = value


    def get(token_obj):
        if token_obj.lexeme in self.data:
            return self.data[token_obj.lexeme]

        raise Exception('Undefined variable {0}'.format(token_obj.lexeme))
