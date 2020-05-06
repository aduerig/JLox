from TokenType import TokenType, Token

class Scanner:
    def __init__(self, lox_instance, text):
        self.lox_instance = lox_instance
        self.text = text
        self.curr_line = 1
        self.index = 0
        self.tokens = []

    
    def scan_tokens(self):
        tokens = []
        while self.index < len(self.text):
            if self.text[self.index] in [' ', '\r', '\t']:
                self.index += 1
                continue
            if self.text[self.index] == '\n':                
                self.index += 1
                self.curr_line += 1
                continue
            self.scan_single_token()

        self.add_token(TokenType.EOF, "")
        return self.tokens


    def add_token(self, token_type, str_value):
        self.tokens.append(Token(token_type, str_value, None, self.curr_line))


    def scan_single_token(self):
        single_char = self.text[self.index]
        token_type = None

        # single
        if single_char == '(': token_type = TokenType.OPEN_PAREN
        elif single_char == ')': token_type = TokenType.CLOSE_PAREN
        elif single_char == '{': token_type = TokenType.OPEN_BRACE
        elif single_char == '}': token_type = TokenType.CLOSE_BRACE
        elif single_char == ',': token_type = TokenType.COMMA
        elif single_char == '.': token_type = TokenType.DOT
        elif single_char == '-': token_type = TokenType.MINUS
        elif single_char == '+': token_type = TokenType.PLUS
        elif single_char == ';': token_type = TokenType.SEMICOLON
        elif single_char == '*': token_type = TokenType.STAR
        elif single_char == '/': token_type = TokenType.SLASH
        
        # single or double
        second_char = None
        if self.index < len(self.text) - 1:
            second_char = self.text[self.index + 1]
        if single_char == '!': 
            if second_char == '=':
                token_type = TokenType.BANG_EQUAL
            else:
                token_type = TokenType.BANG
        elif single_char == '=': 
            if second_char == '=':
                token_type = TokenType.EQUAL_EQUAL
            else:
                token_type = TokenType.EQUAL
        elif single_char == '<': 
            if second_char == '=':
                token_type = TokenType.LESS_EQUAL
            else:
                token_type = TokenType.LESS
        elif single_char == '>': 
            if second_char == '=':
                token_type = TokenType.GREATER_EQUAL
            else:
                token_type = TokenType.GREATER

        # comments
        elif single_char == '~':
            self.index += 1
            while self.index < len(self.text) and self.text[self.index] != '\n':
                self.index += 1
            return

        # String Literal
        elif single_char == '"':
            self.index += 1
            start_quote_index = self.index
            count_newlines = 0
            while self.index < len(self.text) and self.text[self.index] != '"':
                if self.text[self.index] == '\n':
                    count_newlines += 1
                self.index += 1

            if self.index == len(self.text):
                self.lox_instance.raise_error(self.curr_line, "Unterminated string")
                return
            string_literal = self.text[start_quote_index:self.index]
            self.add_token(TokenType.STRING, string_literal)
            self.curr_line += count_newlines
            if self.index != len(self.text):
                self.index += 1
            return

        # Numbers
        elif single_char.isdigit():
            start_number_index = self.index
            self.index += 1
            one_period = 0
            while self.index < len(self.text) and (self.text[self.index].isdigit() or self.text[self.index] == '.'):
                one_period += self.text[self.index] == '.'
                if one_period > 1:
                    self.index += 1
                    self.lox_instance.raise_error(self.curr_line, "Multiple periods in a number parsed")
                    return
                self.index += 1
            number = self.text[start_number_index:self.index]
            self.add_token(TokenType.NUMBER, float(number))
            return

        # Word (Keywords / Variables)
        elif single_char.isalpha():
            start_word_index = self.index
            self.index += 1
            while self.index < len(self.text) and self.text[self.index] not in ['~', ' ', '\r', '\t', '\n']:
                self.index += 1
            word = self.text[start_word_index:self.index]
            keyword_map = {
                'and': TokenType.AND,
                'class': TokenType.CLASS,
                'else': TokenType.ELSE,
                'false': TokenType.FALSE,
                'fun': TokenType.FUN,
                'for': TokenType.FOR,
                'if': TokenType.IF,
                'nil': TokenType.NIL,
                'or': TokenType.OR,
                'print': TokenType.PRINT,
                'return': TokenType.RETURN,
                'super': TokenType.SUPER,
                'this': TokenType.THIS,
                'true': TokenType.TRUE,
                'var': TokenType.VAR,
                'while': TokenType.WHILE,
            }
            if word in keyword_map:
                self.add_token(keyword_map[word], "")
            else:
                self.add_token(TokenType.IDENTIFIER, word)
            return

        if token_type is None:
            self.lox_instance.raise_error(self.curr_line, 
                "Unexpected character {0}".format(single_char))
            return

        self.add_token(token_type, "")
        self.index += 1