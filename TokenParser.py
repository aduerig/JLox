from TokenType import TokenType, Token
import Expression

class Parser:
    def __init__(self, lox_instance, tokens):
        self.lox_instance = lox_instance
        self.tokens = tokens
        self.index = 0
        self.last_line = 1
    

    # def curr_token_is(self, legal_tokens):
    #     return self.index < len(self.tokens) and \
    #         self.tokens[self.index] in legal_tokens

    def raise_if_out_of_range(self):
        if self.index >= len(self.tokens):
            self.lox_instance.raise_error(self.last_line, 
                'PARSER ERROR: Expecting token but out of range')

    def curr_token_is(self, legal_tokens):
        self.raise_if_out_of_range()
        return self.tokens[self.index] in legal_tokens


    def peek(self):
        self.raise_if_out_of_range()
        return self.tokens[self.index]


    def pop_first_token(self):
        self.raise_if_out_of_range()
        curr = self.tokens[self.index]
        self.last_line = curr.line
        self.index += 1
        return curr


    def expression(self):
        return self.equality()


    def equality(self):
        curr_expr = self.comparison()
        equality_ops = [TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL]
        while self.curr_token_is(equality_ops):
            operator = self.pop_first_token()
            right_side = self.comparison()
            curr_expr = expression.Binary(curr_expr, operator, right_side)
        return curr_expr


    def comparison(self):
        curr_expr = self.addition()
        compare_ops = [TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL]
        while self.curr_token_is(compare_ops):
            operator = self.pop_first_token()
            right_side = self.addition()
            curr_expr = expression.Binary(curr_expr, operator, right_side)
        return curr_expr


    def addition(self):
        curr_expr = self.multiplication()
        addition_ops = [TokenType.MINUS, TokenType.PLUS]
        while self.curr_token_is(addition_ops):
            operator = self.pop_first_token()
            right_side = self.multiplication()
            curr_expr = expression.Binary(curr_expr, operator, right_side)
        return curr_expr


    def multiplication(self):
        curr_expr = self.unary()
        mult_ops = [TokenType.STAR, TokenType.SLASH]
        while self.curr_token_is(mult_ops):
            operator = self.pop_first_token()
            right_side = self.unary()
            curr_expr = expression.Binary(curr_expr, operator, right_side)
        return curr_expr


    def unary(self):
        unary_ops = [TokenType.MINUS, TokenType.BANG]
        if self.peek() in unary_ops:
            operator = self.pop_first_token()
            right_side = self.primary()
            return expression.Unary(operator, right_side)
        return self.primary()


    def primary(self):
        if self.peek() == TokenType.OPEN_PAREN:
            paren_expr = self.expression()
            right_paren = self.pop_first_token()
            if right_paren != TokenType.CLOSE_PAREN:
                error_msg = 'PARSER ERROR: Expecting right parenthesis, but got {0}'.format(right_paren)
                self.lox_instance.raise_error(right_paren.line, error_msg)
            return paren_expr

        primary_tokens = [TokenType.NUMBER, TokenType.STRING, TokenType.FALSE, TokenType.TRUE, TokenType.NIL]
        if self.peek() not in primary_tokens:
            error_msg = 'PARSER ERROR: Expecting one of: {0}, but got {1}'.format(primary_tokens, self.peek())
            self.lox_instance.raise_error(right_paren.line, error_msg)
        return self.pop_first_token()