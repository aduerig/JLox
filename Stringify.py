from TokenType import TokenType
from Visitor import Visitor

class Stringify(Visitor):
    def help_indent(self, string):
        tab = '    '
        return tab + string.replace('\n', '\n{0}'.format(tab))


    ## Expression visitors ##
    def visit_binary(self, binary_obj):
        return '(' + binary_obj.left.accept(self) + ' ' + \
            binary_obj.operator.lexeme + ' ' + \
            binary_obj.right.accept(self) + ')'


    def visit_assignment(self, assignment_obj):
        return '{0} = {1}'.format(
            assignment_obj.token_obj.lexeme, assignment_obj.right.accept(self))


    def visit_grouping(self, grouping_obj):
        return '(' + grouping_obj.expression.accept(self) + ')'


    def visit_literal(self, literal_obj):
        return str(literal_obj.value)


    def visit_unary(self, unary_obj):
        return unary_obj.operator.lexeme  + '(' + unary_obj.right.accept(self) + ')'


    def visit_variable(self, variable_obj):
        return variable_obj.token_obj.lexeme


    ## Statement visitors ##
    def visit_expression(self, expression_obj):
        return expression_obj.expression.accept(self)


    def visit_print(self, print_obj):
        return 'print {0}'.format(print_obj.expression.accept(self)) + ';'


    def visit_var(self, var_obj):
        return 'var {0} = {1};'.format(var_obj.token_obj.lexeme, var_obj.initializer.accept(self))


    def visit_function(self, function_obj):
        return 'fun {0}({1})\n{2}'.format(
            function_obj.token_obj.lexeme, 
            ', '.join([x.lexeme for x in function_obj.param_token_objs]), 
            function_obj.body.accept(self))


    def visit_while(self, while_obj):
        body = while_obj.then_branch.accept(self)
        return 'while {0}\n{1}'.format(
            while_obj.condition.accept(self), body)
        # body = while_obj.then_branch.accept(self)
        # indented_body = self.help_indent(body)
        # return 'while {0}\n{{\n{1}\n}}'.format(
        #     while_obj.condition.accept(self), indented_body)


    def visit_block(self, block_obj):
        stringified_statements = '\n'.join([s.accept(self) for s in block_obj.statements])
        indented_stringified_statements = self.help_indent(stringified_statements)
        return '{\n' + indented_stringified_statements + '\n}'
