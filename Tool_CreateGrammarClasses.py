grammer_definition_file = 'basic.gram'
grammer_class_filename_write = 'expression_output.py'


indent = ' ' * 4
base_expression_class_name = 'Expression'
base_visitor_class_name = 'Visitor'
visitor_types = ['Eval', 'Stringify']

def write_visitor_info(write_file, all_expr_class_infos):
    write_file.write("class {0}:\n".format(base_visitor_class_name))
    write_file.write("{0}pass\n".format(indent))
    write_file.write('\n')

    for visitor_type in visitor_types:
        write_file.write("class {0}:\n".format(visitor_type))
        for expr_class_name, field_arr in all_expr_class_infos.items():
            write_file.write("{0}def visit_{1}(self, {2}_obj):\n".format(
                indent, expr_class_name.lower(), expr_class_name.lower()))
            write_file.write("{0}pass\n".format(indent*2))
            write_file.write('\n')


def write_header_info(write_file, all_expr_class_infos):
    write_file.write("# Expression Types:\n")
    write_file.write("# {0}{1}\n".format(indent, ', '.join(all_expr_class_infos.keys())))
    write_file.write("# \n")
    write_file.write("# Visitors (accepts) avaliable on types:\n")
    write_file.write("# {0}{1}\n\n".format(indent, ', '.join(visitor_types)))


def write_expression_base_class(write_file):
    write_file.write("class {0}:\n".format(base_expression_class_name))
    write_file.write("{0}def accept(self, visitor_obj):\n".format(indent))
    write_file.write("{0}visitor_class_name = self.__class__.__name__.lower()\n".format(indent*2))
    write_file.write("{0}method_name = 'visit_' + visitor_class_name\n".format(indent*2))
    write_file.write("{0}func_to_call = getattr(visitor_obj, method_name)\n".format(indent*2))
    write_file.write("{0}return func_to_call(self)\n".format(indent*2))
    write_file.write('\n')


def read_line_from_grammar(write_file, line):
    colon_split = line.split(':')
    if len(colon_split) != 2:
        if 'END GRAMMAR' not in line and line.rstrip().lstrip() != '':
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


def write_expression_classes(write_file, all_expr_class_infos):
    for expr_class_name, expr_class_fields in all_expr_class_infos.items():
        # Set-up for class
        write_file.write("class {0}({1}):\n".format(expr_class_name, base_expression_class_name))
        write_file.write("{0}def __init__({1}):\n".format(
            indent, ', '.join(
                ['self'] + [var_name for var_type, var_name in expr_class_fields])))

        # Writing fields of __init__()
        for field in expr_class_fields:
            (var_type, var_name)  = field
            write_file.write("{0}self.{1} = {2} # type: {3}\n".format(
                indent * 2, var_name, var_name, var_type))    
        write_file.write('\n')


# writing the actual class
with open(grammer_definition_file, 'r') as read_file:
    with open(grammer_class_filename_write, 'w') as write_file:
        for line in read_file:
            if 'START GRAMMAR' in line:
                break

        all_expr_class_infos = {}
        for line in read_file:
            expr_class_info = read_line_from_grammar(write_file, line)
            if expr_class_info:
                all_expr_class_infos.update(expr_class_info)
                print(all_expr_class_infos)
            if 'END GRAMMAR' in line:
                break

        # header
        write_header_info(write_file, all_expr_class_infos)
        
        # visitor info
        write_visitor_info(write_file, all_expr_class_infos)

        # writing expr info
        write_expression_base_class(write_file)

        # writing expr info
        write_expression_classes(write_file, all_expr_class_infos)


# reads file, strips all trailing newlines and stores in temp string
with open(grammer_class_filename_write, 'r') as write_file:
    new_str = write_file.read().rstrip('\n')

# overwrites file with tempstring
with open(grammer_class_filename_write, 'w') as write_file:
    write_file.write(new_str)

print('Created "{0}" file from "{1}" file'.format(
    grammer_class_filename_write, grammer_definition_file))