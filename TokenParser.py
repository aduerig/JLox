from TokenType import TokenType, Token
import Expression
import Statement


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, lox_instance, tokens):
        self.lox_instance = lox_instance
        self.tokens = tokens
        self.index = 0
        self.last_line = 1
    

    # def curr_token_is(self, legal_tokens):
    #     return self.index < len(self.tokens) and \
    #         self.tokens[self.index] in legal_tokens

    # parses the list of expressions given to the class
    def parse(self):
        try:
            print('PARSER: started')
            statements = []
            while self.tokens[self.index].token_type != TokenType.EOF:
                statements.append(self.declaritive_statement())
            print('PARSER: gracefully ended')
            return statements
        except ParseError:
            print('PARSER: NOT gracefully ended')
            return None
        except Exception as e:
            print('PARSER: EXTREMELY ungracefully ended')
            raise e


    # def raise_if_out_of_range(self):
        # if self.index >= len(self.tokens):
            # self.lox_instance.raise_error(self.last_line, 
                # 'PARSER ERROR: Expecting token but out of range')


    def curr_token_is(self, legal_tokens):
        # self.raise_if_out_of_range()
        return self.tokens[self.index].token_type in legal_tokens


    # def peek(self):
    #     # self.raise_if_out_of_range()
    #     return self.tokens[self.index]


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
            exception_msg = 'pop_token_expect: was expecting a type from'.format(expecting_type_arr)
            if given_exception_msg:
                exception_msg = given_exception_msg
            raise Exception(exception_msg)
        self.last_line = curr.line
        self.index += 1
        return curr


    def declaritive_statement(self):
        try:
            if self.curr_token_is([TokenType.VAR]):
                return self.var_statement()
            return self.statement()
        # Implement syncronization of parsing errors here
        except Exception as e:
            raise e

    
    def var_statement(self):
        self.pop_token()
        identifier_token = self.pop_token_expect([TokenType.IDENTIFIER], 'Expecting variable name')
        if self.curr_token_is([TokenType.EQUAL]):
            self.pop_token()
            initializer_expression = self.expression()
        self.pop_token_expect([TokenType.SEMICOLON], 'Expecting semicolon after variable declaration / assignment')
        return Statement.Var(identifier_token, initializer_expression)


    def statement(self):
        if self.curr_token_is([TokenType.PRINT]):
            return self.print_statement()
        return self.expression_statement()


    def print_statement(self):
        # print('new print_statement', self.index, self.tokens[self.index:])
        self.pop_token()
        expression = self.expression()
        self.pop_token_expect([TokenType.SEMICOLON])
        return Statement.Print(expression)


    def expression_statement(self):
        # print('new expression_statement', self.index, self.tokens[self.index:])
        expression = self.expression()
        self.pop_token_expect([TokenType.SEMICOLON])
        return Statement.Expression(expression)


    def expression(self):
        # print('new expression', self.index, self.tokens[self.index:])
        return self.equality()


    def equality(self):
        # print('equality', self.index)
        curr_expr = self.comparison()
        equality_ops = [TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL]
        while self.curr_token_is(equality_ops):
            operator = self.pop_token()
            # print('equality looking for right side', self.index)
            right_side = self.comparison()
            curr_expr = Expression.Binary(curr_expr, operator, right_side)
        return curr_expr


    def comparison(self):
        # print('comparison', self.index)
        curr_expr = self.addition()
        compare_ops = [TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL]
        while self.curr_token_is(compare_ops):
            operator = self.pop_token()
            right_side = self.addition()
            curr_expr = Expression.Binary(curr_expr, operator, right_side)
        return curr_expr


    def addition(self):
        # print('addition', self.index)
        curr_expr = self.multiplication()
        addition_ops = [TokenType.MINUS, TokenType.PLUS]
        while self.curr_token_is(addition_ops):
            operator = self.pop_token()
            right_side = self.multiplication()
            curr_expr = Expression.Binary(curr_expr, operator, right_side)
        return curr_expr


    def multiplication(self):
        # print('multiplication', self.index)
        curr_expr = self.unary()
        mult_ops = [TokenType.STAR, TokenType.SLASH]
        while self.curr_token_is(mult_ops):
            operator = self.pop_token()
            right_side = self.unary()
            curr_expr = Expression.Binary(curr_expr, operator, right_side)
        return curr_expr


    def unary(self):
        # print('unary', self.index)
        unary_ops = [TokenType.MINUS, TokenType.BANG]
        if self.curr_token_is(unary_ops):
            operator = self.pop_token()
            right_side = self.primary()
            return Expression.Unary(operator, right_side)
        return self.primary()


    def primary(self):
        # print('primary', self.index)
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