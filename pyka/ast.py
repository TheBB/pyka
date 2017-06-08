class ASTNode:
    pass


class Symbol(ASTNode):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{{sym {self.name}}}'


class Number(ASTNode):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{{num {self.value}}}'


class BinOp(ASTNode):

    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return f'{{bop {self.op} {self.lhs} {self.rhs}}}'


class Call(ASTNode):

    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __repr__(self):
        return f'{{call {self.func} {self.args}}}'


class Prototype(ASTNode):

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f'{{prt {self.name or "??"} {self.args}}}'


class Definition(ASTNode):

    def __init__(self, prototype, body):
        self.prototype = prototype
        self.body = body

    def __repr__(self):
        return f'{{def {self.prototype} {self.body}}}'


class ExprWrapper(Definition):

    def __init__(self, body):
        super(ExprWrapper, self).__init__(Prototype(None, []), body)
