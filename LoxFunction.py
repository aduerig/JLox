import time

class LoxFunction:
    def __init__(self, declaration):
        self.declaration = declaration


    def arity(self):
        return len(self.declaration.param_token_objs)
    

    def call(self, intepretor, argument_values):
        new_scope = {'#parent_level#': intepretor.global_data_scope}
        for param_token_obj, argument_value in zip(self.declaration.param_token_objs, argument_values):
            intepretor.define(new_scope, param_token_obj, argument_value)
        intepretor.execute_block_with_scope(new_scope, self.declaration.body)
    

    def __str__(self):
        return "<function " + self.declaration.token_obj.lexeme + ">"


class ClockLoxFunction(LoxFunction):
    """Returns time in seconds since unix epoch. Arguments: {}"""
    def __init__(self):
        pass

    
    def arity(self):
        return 0

    
    def call(self, intepretor, arg_token_objs):
        return time.time()
    

    def __str__(self):
        return 'native clock() function, calls into python.time(). Returns time in seconds since unix epoch.'