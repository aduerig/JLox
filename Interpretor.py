from TokenType import TokenType, Token
from Visitor import Visitor


# Evaluates statements + expressions
class Interpretor(Visitor):
    def __init__(self, lox_instance):
        self.lox_instance = lox_instance
        self.data = {'#parent_level#': None}

    
    def interpret(self, statements):
        for statement in statements:
            statement.accept(self)


    def define(self, token_obj, value):
        self.data[token_obj.lexeme] = value


    def assign(self, token_obj, value):
        curr_level = self.data
        while curr_level:
            if token_obj.lexeme in curr_level:
                curr_level[token_obj.lexeme] = value
                return
            curr_level = curr_level['#parent_level#']
        raise Exception('Variable {0} not defined. Line {1}: Please '.format(
                token_obj.lexeme, token_obj.line) + 'use var to define the variable before assignment')


    def get(self, token_obj):
        curr_level = self.data
        while curr_level:
            if token_obj.lexeme in curr_level:
                return curr_level[token_obj.lexeme]
            curr_level = curr_level['#parent_level#']
        raise Exception('Undefined variable {0}'.format(token_obj))


    def evaluate(self, expression):
        return expression.accept(self)
    

    ## Statement visitors ##
    def visit_block(self, block_obj):
        new_scoped_data = {'#parent_level#': self.data}
        self.data = new_scoped_data
        self.interpret(block_obj.statements)
        self.data = self.data['#parent_level#']
        # print('left')


    def visit_expression(self, expression_obj):
        expression_obj.expression.accept(self)

    
    def visit_if(self, if_obj):
        if self.evaluate(if_obj.condition):
            return self.evaluate(if_obj.then_branch)
        if if_obj.else_branch:
            return self.evaluate(if_obj.else_branch)


    def visit_print(self, print_obj):
        print(print_obj.expression.accept(self))


    def visit_var(self, var_obj):
        result = None
        if var_obj.initializer:
            result = self.evaluate(var_obj.initializer)
        self.define(var_obj.token_obj, result)


    ## Expression land ##
    # helper function
    def is_truthy(self, value):
        if value is bool or value is None:
            return False
        return True


    ## Expression visitors ##
    def visit_assignment(self, assignment_obj):
        evaluated_expression = self.evaluate(assignment_obj.right)
        self.assign(assignment_obj.token_obj, evaluated_expression)
        return evaluated_expression


    def visit_binary(self, binary_expression):
        left_evaled = self.evaluate(binary_expression.left)
        right_evaled = self.evaluate(binary_expression.right)
        # need to add a ton of type checks
        f_map = {
            TokenType.PLUS: lambda a, b: a + b,
            TokenType.MINUS: lambda a, b: a - b,
            TokenType.STAR: lambda a, b: a * b,
            TokenType.SLASH: lambda a, b: a / b,
            TokenType.EQUAL_EQUAL: lambda a, b: a == b,
            TokenType.BANG_EQUAL: lambda a, b: a != b,
            TokenType.LESS: lambda a, b: a < b,
            TokenType.LESS_EQUAL: lambda a, b: a <= b,
            TokenType.GREATER: lambda a, b: a > b,
            TokenType.GREATER_EQUAL: lambda a, b: a >= b,
        }
        return f_map[binary_expression.operator.token_type](left_evaled, right_evaled)


    def visit_grouping(self, grouping_expression):
        return self.evaluate(grouping_expression.expression)


    def visit_literal(self, literal_expression):
        return literal_expression.value


    def visit_unary(self, unary_expression):
        evaled = self.evaluate(unary_expression.right)
        if unary_expression.operator.token_type == TokenType.MINUS:
            return -evaled
        elif unary_expression.operator.token_type == TokenType.BANG:
            return not self.is_truthy(evaled)
        else:
            raise Exception('ok?')


    def visit_variable(self, variable_obj):
        return self.get(variable_obj.token_obj)