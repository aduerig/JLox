import argparse

# my imports
from CharacterScanner import Scanner
from TokenParser import Parser
from Interpretor import Interpretor

# will delete
# from VisitExpression import EvaluateExpression, StringifyExpression
# from VisitStatement import StringifyStatement, EvaluateStatement


class Lox:
    def __init__(self, filename = None):
        self.has_errored = False
        if filename is None:
            self.run_prompt()
        else:
            self.run_file(filename)


    def run_file(self, filename):
        with open(filename) as file:
            self.run(file.read())


    def run_prompt(self):
        while True:
            user_input = input('> ')
            self.run(user_input)
            self.has_errored = False

    
    def run(self, text):
        # Scanning: characters -> tokens
        print('JLOX: scanning characters')
        scanner = Scanner(self, text)
        all_tokens = scanner.scan_tokens()

        # Parsing: tokens -> statements
        print('JLOX: parsing tokens into statements')
        token_parser = Parser(self, all_tokens)
        statements = token_parser.parse()
        
        # Intepreting: evaluating statements
        interpretor = Interpretor(self)
        print('JLOX: Execution beginning...')
        interpretor.interpret(statements)
        print('JLOX: Execution ended...')

    def raise_error_with_token(self, token, message):
        self.has_errored = True
        self.report_error(token.line, token, message)


    def raise_error(self, line, message):
        self.has_errored = True
        self.report_error(line, "", message)


    def report_error(self, line, where, message):
        print('ERROR : [line: {0}] : {1} : {2}'.format(line, where, message))


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-filename", default=None, type=str, help="Enter the filename you want Lox to run")
    arg_parser.parse_args()

    # filename = arg_parser.filename

    # For testing, commment out for CIL args
    filename = 'test_script3.lox'
    
    # runs file
    if filename:
        Lox(filename)
    # runs prompt
    else:
        Lox()