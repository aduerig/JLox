from TokenType import TokenType, Token
import Expression
import Statement
from Stringify import Stringify


class ParseError(Exception):
    pass

class Parser:
    def __init__(self, lox_instance, tokens):
        self.lox_instance = lox_instance
        self.tokens = tokens
        self.index = 0
        self.last_line = 1
    
    
    def at_end_of_tokens(self):
        return self.tokens[self.index].token_type == TokenType.EOF

    # parses the list of expressions given to the class
    def parse(self):
        try:
            print('PARSER: started')
            statements = []
            while not self.at_end_of_tokens():
                statements.append(self.declaritive_statement())
            print('PARSER: gracefully ended')
            return statements
        except ParseError:
            print('PARSER: NOT gracefully ended')
            return None
        except Exception as e:
            print('PARSER: EXTREMELY ungracefully ended')
            raise e


    def peek(self):
        return self.tokens[self.index]


    # def raise_if_out_of_range(self):
        # if self.index >= len(self.tokens):
            # self.lox_instance.raise_error(self.last_line, 
                # 'PARSER ERROR: Expecting token but out of range')


    def curr_token_is(self, legal_tokens):
        # self.raise_if_out_of_range()
        return self.tokens[self.index].token_type in legal_tokens


    def pop_token(self):
        # self.raise_if_out_of_range()
        curr = self.tokens[self.index]
        self.last_line = curr.line
        self.index += 1
        return curr


    def pop_token_expect(self, expecting_type_arr, given_exception_msg = None):
        # self.raise_if_out_of_range()
        curr = self.tokens[self.index]
        if curr.token_type not in expecting_type_arr:
            exception_msg = 'pop_token_expect: was expecting a type from {0}'.format(expecting_type_arr)
            if given_exception_msg:
                exception_msg = given_exception_msg
            raise Exception(exception_msg + ', got: {0}'.format(curr))
        self.last_line = curr.line
        self.index += 1
        return curr

    ## Statements ##
    def declaritive_statement(self):
        try:
            if self.curr_token_is([TokenType.RETURN]):
                return self.return_statement()
            elif self.curr_token_is([TokenType.FUN]):
                return self.function_declaration()
            elif self.curr_token_is([TokenType.VAR]):
                return self.var_statement()
            return self.statement()
        # Implement syncronization of parsing errors here
        except Exception as e:
            raise e


    def return_statement(self):
        self.pop_token()
        return_expression = self.expression()
        self.pop_token_expect([TokenType.SEMICOLON], 'Expecting a ; after return parameter')

        return_statement = Statement.Return(return_expression)
        return return_statement


    def function_declaration(self):
        self.pop_token()
        name_token_obj = self.pop_token_expect([TokenType.IDENTIFIER], 'Expecting name for function after "fun"')
        self.pop_token_expect([TokenType.OPEN_PAREN], 'Expecting opening ( during function declaration')
        
        param_token_objs = []
        while not self.curr_token_is([TokenType.CLOSE_PAREN]):
            param_token_objs.append(self.pop_token_expect(
                [TokenType.IDENTIFIER], 'Expecting indentifier for function parameters'))
            if self.curr_token_is([TokenType.CLOSE_PAREN]):
                break
            self.pop_token_expect([TokenType.COMMA], 'Expecting a ) or a , after function parameter')
        
        self.pop_token_expect([TokenType.CLOSE_PAREN], 'Expecting closing ) during function declaration')
        if not self.curr_token_is([TokenType.OPEN_BRACE]):
            raise Exception('Expecting opening brace after function registration')
        body = self.block_statement()
        function_def = Statement.Function(name_token_obj, param_token_objs, body)
        return function_def

    
    def var_statement(self):
        self.pop_token()
        identifier_token = self.pop_token_expect([TokenType.IDENTIFIER], 'Expecting variable name')
        initializer_expression = None
        if self.curr_token_is([TokenType.EQUAL]):
            self.pop_token()
            initializer_expression = self.expression()
        self.pop_token_expect([TokenType.SEMICOLON], 'Expecting semicolon after variable declaration / assignment')
        return Statement.Var(identifier_token, initializer_expression)


    def statement(self):
        if self.curr_token_is([TokenType.WHILE]):
            return self.while_statement()
        elif self.curr_token_is([TokenType.FOR]):
            return self.for_statement()
        elif self.curr_token_is([TokenType.IF]):
            return self.if_statement()
        elif self.curr_token_is([TokenType.MAYBE]):
            return self.maybe_statement()
        elif self.curr_token_is([TokenType.PRINT]):
            return self.print_statement()
        elif self.curr_token_is([TokenType.OPEN_BRACE]):
            return self.block_statement()
        return self.expression_statement()


    def while_statement(self):
        self.pop_token()
        condition = self.expression()
        if not self.curr_token_is([TokenType.OPEN_BRACE]):
            raise Exception('while statement needs a {\} block after it')
        then_branch = self.block_statement()
        return Statement.While(condition, then_branch)


    def for_statement(self):
        self.pop_token()
        self.pop_token_expect([TokenType.OPEN_PAREN], 'For loop needs an opening parenthesis')
        initializer = self.declaritive_statement()
        condition = self.expression()
        self.pop_token_expect([TokenType.SEMICOLON], 'Need a semicolon after the condition in the for loop')
        after_expression = self.expression()
        self.pop_token_expect([TokenType.CLOSE_PAREN], 'For loop needs a closing parenthesis')
        then_branch = self.block_statement()

        wrapped_while_body = Statement.Block([then_branch, after_expression])
        while_statement = Statement.While(condition, wrapped_while_body)
        the_statements = [
            initializer,
            while_statement
        ]
        # print(Statement.Block(the_statements).accept(Stringify()))
        return Statement.Block(the_statements)


    def if_statement(self):
        self.pop_token()
        condition = self.expression()
        if not self.curr_token_is([TokenType.OPEN_BRACE]):
            raise Exception('if statement needs a { after it', self.pop_token())
        then_branch = self.block_statement()
        
        else_branch = None
        if self.curr_token_is([TokenType.ELSE]):
            self.pop_token()
            if not self.curr_token_is([TokenType.OPEN_BRACE]):
                raise Exception('else statement needs a { after it')
            else_branch = self.block_statement()
        return Statement.If(condition, then_branch, else_branch)


    def maybe_statement(self):
        self.pop_token()
        if not self.curr_token_is([TokenType.OPEN_BRACE]):
            raise Exception('maybe statement needs a {\} block after it')
        then_branch = self.block_statement()
        return Statement.Maybe(then_branch)


    def print_statement(self):
        self.pop_token()
        expression = self.expression()
        self.pop_token_expect([TokenType.SEMICOLON])
        return Statement.Print(expression)


    def block_statement(self):
        self.pop_token()
        statements = []
        while not self.at_end_of_tokens() and not self.curr_token_is([TokenType.CLOSE_BRACE]):
            statements.append(self.declaritive_statement())
        if self.at_end_of_tokens():
            raise Exception('Missing }, program ended before block closed')
        self.pop_token()
        return Statement.Block(statements)


    def expression_statement(self):
        expression = self.expression()
        self.pop_token_expect([TokenType.SEMICOLON])
        return Statement.Expression(expression)


    ## Expressions ##
    def expression(self):
        return self.assignment()


    def assignment(self):
        curr_expr = self.logical_ops()
        if self.curr_token_is([TokenType.EQUAL]):
            self.pop_token()
            right_side = self.assignment()
            if isinstance(curr_expr, Expression.Variable):
                return Expression.Assignment(curr_expr.token_obj, right_side)
            raise Exception('PARSER: Invalid assignment target {0}'.format(curr_expr.accept(Stringify())))
        return curr_expr

    
    def logical_ops(self):
        curr_expr = self.equality()
        logical_ops = [TokenType.OR, TokenType.AND]
        while self.curr_token_is(logical_ops):
            operator = self.pop_token()
            right_side = self.equality()
            curr_expr = Expression.Binary(curr_expr, operator, right_side)
        return curr_expr        


    def equality(self):
        curr_expr = self.comparison()
        equality_ops = [TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL]
        while self.curr_token_is(equality_ops):
            operator = self.pop_token()
            right_side = self.comparison()
            curr_expr = Expression.Binary(curr_expr, operator, right_side)
        return curr_expr


    def comparison(self):
        curr_expr = self.addition()
        compare_ops = [TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL]
        while self.curr_token_is(compare_ops):
            operator = self.pop_token()
            right_side = self.addition()
            curr_expr = Expression.Binary(curr_expr, operator, right_side)
        return curr_expr


    def addition(self):
        curr_expr = self.multiplication()
        addition_ops = [TokenType.MINUS, TokenType.PLUS]
        while self.curr_token_is(addition_ops):
            operator = self.pop_token()
            right_side = self.multiplication()
            curr_expr = Expression.Binary(curr_expr, operator, right_side)
        return curr_expr


    def multiplication(self):
        curr_expr = self.unary()
        mult_ops = [TokenType.STAR, TokenType.SLASH, TokenType.PERCENT]
        while self.curr_token_is(mult_ops):
            operator = self.pop_token()
            right_side = self.unary()
            curr_expr = Expression.Binary(curr_expr, operator, right_side)
        return curr_expr


    def unary(self):
        unary_ops = [TokenType.MINUS, TokenType.BANG]
        if self.curr_token_is(unary_ops):
            operator = self.pop_token()
            right_side = self.function_call()
            return Expression.Unary(operator, right_side)
        return self.function_call()


    def finish_call(self, curr_expr):
        args = []
        if not self.curr_token_is([TokenType.CLOSE_PAREN]):
            args.append(self.expression())
            while self.curr_token_is([TokenType.COMMA]):
                self.pop_token()
                args.append(self.expression())
        closing_paren = self.pop_token_expect([TokenType.CLOSE_PAREN], 'Expect ) after arguments of function call')
        return Expression.Call(curr_expr, closing_paren, args)


    def function_call(self):
        curr_expr = self.primary()
        while True:
            if self.curr_token_is([TokenType.OPEN_PAREN]):
                self.pop_token()
                curr_expr = self.finish_call(curr_expr)
            else:
                break
        return curr_expr


    def primary(self):
        if self.curr_token_is([TokenType.OPEN_PAREN]):
            self.pop_token()
            paren_expr = self.expression()
            self.pop_token_expect([TokenType.CLOSE_PAREN], 'PARSER ERROR: Expecting right parenthesis')
            return Expression.Grouping(paren_expr)

        primary_tokens = [TokenType.NUMBER, TokenType.STRING, TokenType.FALSE, TokenType.TRUE, TokenType.NIL, TokenType.IDENTIFIER]
        curr_token = self.pop_token()
        if curr_token.token_type not in primary_tokens:
            error_msg = 'PARSER ERROR: Expecting one of: {0}, but got {1}'.format(primary_tokens, curr_token.token_type)
            self.lox_instance.raise_error_with_token(curr_token, error_msg)
            raise ParseError()

        if curr_token.token_type == TokenType.IDENTIFIER:
            return Expression.Variable(curr_token)

        primary_token_map = {
            TokenType.NUMBER: curr_token.literal,
            TokenType.STRING: curr_token.literal,
            TokenType.FALSE: False,
            TokenType.TRUE: True,
            TokenType.NIL: None
        }
        return Expression.Literal(primary_token_map[curr_token.token_type])