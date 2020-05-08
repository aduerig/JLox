from TokenType import TokenType, Token
from VisitExpression import EvaluateExpression


# not needed yet? most is crammed into Expression.py
class Interpretor:
    def __init__(self, lox_instance):
        self.lox_instance = lox_instance
        self.tokens = tokens
        self.index = 0
        self.last_line = 1

    
    def interpret(self, expression):
        return expression.accept(Eval)