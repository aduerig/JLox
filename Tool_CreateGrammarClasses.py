def write_visitor_info(write_file, all_expr_class_infos):
    write_file.write("class {0}:\n".format(base_visitor_class_name))
    write_file.write("{0}def accept(self, obj):\n".format(indent))
    write_file.write("{0}visitor_class_name = obj.__class__.__name__.lower()\n".format(indent*2))
    write_file.write("{0}method_name = 'visit_' + visitor_class_name\n".format(indent*2))
    write_file.write("{0}func_to_call = getattr(self, method_name)\n".format(indent*2))
    write_file.write("{0}return func_to_call(obj)\n".format(indent*2))
    write_file.write('\n')

    write_file.write("# Implementation for these visitor classes / functions defined elsewhere\n")
    for visitor_type in visitor_types:
        write_file.write("class {0}:\n".format(visitor_type))
        for expr_class_name, field_arr in all_expr_class_infos.items():
            write_file.write("{0}def visit_{1}(self, {2}_obj):\n".format(
                indent, expr_class_name.lower(), expr_class_name.lower()))
            write_file.write("{0}pass\n".format(indent*2))
            write_file.write('\n')


def write_header_info(write_file, all_expr_class_infos, base_class_name):
    write_file.write("# {0} Types:\n".format(base_class_name))
    write_file.write("# {0}{1}\n".format(indent, ', '.join(all_expr_class_infos.keys())))
    write_file.write("# \n")
    write_file.write("# Visitors (accepts) avaliable on types:\n")
    write_file.write("# {0}{1}\n\n".format(indent, ', '.join(visitor_types)))


def write_base_class(write_file, base_class_name):
    write_file.write("class {0}:\n".format(base_class_name))
    write_file.write("{0}def accept(self, visitor_obj):\n".format(indent))
    write_file.write("{0}visitor_obj.visit(self)\n".format(indent*2))
    write_file.write('\n')


def read_line_from_grammar(write_file, line):
    colon_split = line.split(':')
    if len(colon_split) != 2:
        if line.rstrip().lstrip() != '':
            print('Could not parse line in grammar', line)
        return None

    class_name = colon_split[0].replace(' ', '')
    read_obj = {class_name: []}

    # reading fields
    fields = colon_split[1].split(',')
    for field in fields:
        var_type, var_name  = field.lstrip().rstrip().split(' ')
        read_obj[class_name].append((var_type, var_name))
    return read_obj


def write_classes(write_file, all_expr_class_infos, base_class_name):
    for expr_class_name, expr_class_fields in all_expr_class_infos.items():
        # Set-up for class
        write_file.write("class {0}({1}):\n".format(expr_class_name, base_class_name))
        write_file.write("{0}def __init__({1}):\n".format(
            indent, ', '.join(
                ['self'] + [var_name for var_type, var_name in expr_class_fields])))

        # Writing fields of __init__()
        for field in expr_class_fields:
            (var_type, var_name)  = field
            write_file.write("{0}self.{1} = {2} # type: {3}\n".format(
                indent * 2, var_name, var_name, var_type))    
        write_file.write('\n')


base_expression_class_name = 'Expression'
expression_grammar_definition = [
    'Assignment : Token name, Expr right',
    'Binary     : Expr left, Token operator, Expr right',
    'Grouping   : Expr expression',
    'Literal    : Object value',
    'Unary      : Token operator, Expr right',
    'Variable   : Token token_obj',
]
expression_grammar = (base_expression_class_name, expression_grammar_definition)


base_statement_class_name = 'Statement'
statement_grammar_definition = [
    'Block      : List<Statement> statements',
    'Expression : Expr expression',          
    'If         : Expr condition, Statement then_branch, Statemenet else_branch',
    'Print      : Expr expression',
    'Var        : Token name, Expr initializer',
]
statement_grammar = (base_statement_class_name, statement_grammar_definition)


all_grammars = [expression_grammar, statement_grammar]
for base_class_name, grammar_definition in all_grammars:
    # setup stuff for grammar
    grammer_class_filename_write = '{0}_output.py'.format(base_class_name.lower())
    indent = ' ' * 4
    base_visitor_class_name = 'Visitor'
    visitor_types = [
        'Evaluate{0}'.format(base_class_name), 
        'Stringify{0}'.format(base_class_name), 
        # 'Stringify{0}RPN'.format(base_class_name)
    ]
    # writing the actual class
    with open(grammer_class_filename_write, 'w') as write_file:
        all_expr_class_infos = {}
        for line in grammar_definition:
            expr_class_info = read_line_from_grammar(write_file, line)
            if expr_class_info:
                all_expr_class_infos.update(expr_class_info)
                print(all_expr_class_infos)
            if 'END GRAMMAR' in line:
                break

        # header
        write_header_info(write_file, all_expr_class_infos, base_class_name)
        
        # writing expr info
        write_base_class(write_file, base_class_name)

        # writing expr info
        write_classes(write_file, all_expr_class_infos, base_class_name)

        # visitor info
        write_visitor_info(write_file, all_expr_class_infos)

    # reads file, strips all trailing newlines and stores in temp string
    with open(grammer_class_filename_write, 'r') as write_file:
        new_str = write_file.read().rstrip('\n')

    # overwrites file with tempstring
    with open(grammer_class_filename_write, 'w') as write_file:
        write_file.write(new_str)

    print('Created "{0}" file using {1} grammar'.format(
        grammer_class_filename_write, grammar_definition))