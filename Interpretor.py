import random

from TokenType import TokenType, Token
from Visitor import Visitor
from LoxFunction import LoxFunction, ClockLoxFunction
from Stringify import Stringify


class ReturnValue(Exception):
    def __init__(self, expression_evaluated):
        self.expression_evaluated = expression_evaluated


# Evaluates statements + expressions
class Interpretor(Visitor):
    def __init__(self, lox_instance):
        self.lox_instance = lox_instance
        self.local_data_scope = {'#parent_level#': None}
        self.global_data_scope = self.local_data_scope

        ## Registering foreign functions ##
        self.global_data_scope['clock'] = ClockLoxFunction()


    ## Execution helpers ##
    def interpret(self, statements):
        for statement in statements:
            try:
                statement.accept(self)
            except ReturnValue as ret_value:
                return ret_value.expression_evaluated


    def evaluate(self, expression):
        return expression.accept(self)
    

    # implement
    def execute_block_with_scope(self, scope, block_obj):
        save = self.local_data_scope
        self.local_data_scope = scope
        ok = self.interpret(block_obj.statements)
        self.local_data_scope = save
        return ok


    def define(self, scope, token_obj, value):
        scope[token_obj.lexeme] = value


    ## Variabled / Identifiers / Function helpers ##
    def assign(self, scope, token_obj, value):
        while scope:
            if token_obj.lexeme in scope:
                scope[token_obj.lexeme] = value
                return
            scope = scope['#parent_level#']
        raise Exception('Variable {0} not defined. Line {1}: Please '.format(
                token_obj.lexeme, token_obj.line) + 'use var to define the variable before assignment')


    def get(self, scope, token_obj):
        while scope:
            if token_obj.lexeme in scope:
                return scope[token_obj.lexeme]
            scope = scope['#parent_level#']
        raise Exception('Undefined variable {0}'.format(token_obj))


    ## Statement visitors ##
    def visit_block(self, block_obj):
        new_scope = {'#parent_level#': self.local_data_scope}
        self.execute_block_with_scope(new_scope, block_obj)


    def visit_return(self, return_obj):
        raise ReturnValue(self.evaluate(return_obj.expression))


    def visit_expression(self, expression_obj):
        expression_obj.expression.accept(self)


    def visit_while(self, while_obj):
        while self.is_truthy(self.evaluate(while_obj.condition)):
            self.evaluate(while_obj.then_branch)


    def visit_maybe(self, maybe_obj):
        if random.randint(0, 1) == 0:
            self.evaluate(maybe_obj.then_branch)


    def visit_function(self, function_obj):
        new_loc_function = LoxFunction(function_obj)
        self.define(self.local_data_scope, function_obj.token_obj, new_loc_function)


    def visit_if(self, if_obj):
        if self.evaluate(if_obj.condition):
            self.evaluate(if_obj.then_branch)
        elif if_obj.else_branch:
            self.evaluate(if_obj.else_branch)


    def visit_print(self, print_obj):
        print(print_obj.expression.accept(self))


    def visit_var(self, var_obj):
        result = None
        if var_obj.initializer:
            result = self.evaluate(var_obj.initializer)
        self.define(self.local_data_scope, var_obj.token_obj, result)


    ## Expression land ##
    # helper for truthiness
    def is_truthy(self, value):
        if value is False or value is None:
            return False
        return True


    # Helpers for visit_binary
    def logical_op_helper(self, op_token, binary_expression):
        if op_token == TokenType.OR: 
            left_evaled = self.evaluate(binary_expression.left)
            if self.is_truthy(left_evaled):
                return left_evaled
        else:
            left_evaled = self.evaluate(binary_expression.left)
            if not self.is_truthy(left_evaled):
                return left_evaled
        return self.evaluate(binary_expression.right)


    ## Expression visitors ##
    def visit_assignment(self, assignment_obj):
        evaluated_expression = self.evaluate(assignment_obj.right)
        self.assign(self.local_data_scope, assignment_obj.token_obj, evaluated_expression)
        return evaluated_expression


    def visit_binary(self, binary_expression):
        op_token = binary_expression.operator.token_type
        if op_token in [TokenType.OR, TokenType.AND]:
            return self.logical_op_helper(op_token, binary_expression)

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
            TokenType.PERCENT: lambda a, b: a % b,
        }
        return f_map[op_token](left_evaled, right_evaled)


    def visit_call(self, call_obj):
        lox_function = self.evaluate(call_obj.callee)
        if not isinstance(lox_function, LoxFunction):
            raise Exception('{0} is not an identifier, cannot call a function on it'.format(call_obj.callee))
        evaled_args = [self.evaluate(arg) for arg in call_obj.argument_values]
        if len(evaled_args) != lox_function.arity():
            raise Exception('Passed {0} argument_values to {1}, required {2}'.format(
                len(evaled_args), lox_function.declaration.accept(Stringify()), lox_function.arity()))
        return lox_function.call(self, evaled_args)


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
        return self.get(self.local_data_scope, variable_obj.token_obj)