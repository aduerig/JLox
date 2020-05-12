import argparse
import sys

# my imports
from CharacterScanner import Scanner
from TokenParser import Parser
from Interpretor import Interpretor


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


# To disable python's stack trace
def excepthook(type, value, traceback):
    print(value)


def disable_python_stack_trace():
    print('JLOX: WARNING! Diasbling Python stack trace')
    sys.excepthook = excepthook


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-e', '--enable_stack_trace', default=False, action='store_true', help="enables python stack trace")
    arg_parser.add_argument('-i', '--interactive', default=False, action='store_true', help="interactive")
    arg_parser.add_argument('-f', '--filename', default=None, type=str, help="Enter the filename you want Lox to run")
    args = arg_parser.parse_args()


    # interactive prompt
    print(args)
    if not args.enable_stack_trace:
        disable_python_stack_trace()

    # interactive prompt
    if args.interactive:
        Lox()

    # for no argument testing
    filename = args.filename
    if not filename:
        filename = 'test_script2.lox'
        # filename = 'test_script3.lox'

    # runs file
    Lox(filename)
