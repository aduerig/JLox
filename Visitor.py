class Visitor:
    def visit(self, obj):
        visitor_class_name = obj.__class__.__name__.lower()
        method_name = 'visit_' + visitor_class_name
        func_to_call = getattr(self, method_name)
        return func_to_call(obj)