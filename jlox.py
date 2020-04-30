from scanner import Scanner

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
        scanner = Scanner(self, text)
        all_tokens = scanner.scan_tokens()

        for token in all_tokens:
            print(token)


    def raise_error(self, line, message):
        self.has_errored = True
        self.report_error(line, "", message)


    def report_error(self, line, where, message):
        print('ERROR : [line: {0}] : {1} : {2}'.format(line, where, message))


if __name__ == "__main__":
    # runs file
    filename = 'test_script.lox'
    Lox(filename)

    # runs prompt
    # Lox()