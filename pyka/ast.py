import llvmlite.ir as ir


class ASTNode:
    pass


class Symbol(ASTNode):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{{sym {self.name}}}'

    def __str__(self):
        return self.name

    def codegen(self, gen, bld, loc):
        return self.lookup(loc)

    def lookup(self, loc):
        return loc[self.name]


class Number(ASTNode):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{{num {self.value}}}'

    def codegen(self, gen, bld, loc):
        return ir.Constant(ir.DoubleType(), self.value)


class BinOp(ASTNode):

    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return f'{{bop {self.op} {self.lhs!r} {self.rhs!r}}}'

    def codegen(self, gen, bld, loc):
        lhs = self.lhs.codegen(gen, bld, loc)
        rhs = self.rhs.codegen(gen, bld, loc)
        if self.op == '+':
            return bld.fadd(lhs, rhs)
        elif self.op == '-':
            return bld.fsub(lhs, rhs)
        elif self.op == '*':
            return bld.fmul(lhs, rhs)
        elif self.op == '/':
            return bld.fdiv(lhs, rhs)


class Call(ASTNode):

    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __repr__(self):
        return f'{{call {self.func!r} {self.args!r}}}'

    def codegen(self, gen, bld, loc):
        callee = gen.function(str(self.func))
        args = [arg.codegen(gen, bld, loc) for arg in self.args]
        return bld.call(callee, args)


class Prototype(ASTNode):

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        if self.name:
            return f'{{prt {self.name!r} {self.args!r}}}'
        return f'{{prt {self.args!r}}}'

    def __str__(self):
        return str(self.name)

    def codegen(self, gen, mod, loc):
        type_ = ir.FunctionType(ir.DoubleType(), [ir.DoubleType() for _ in self.args])
        name = str(self.name or gen.name())
        func = ir.Function(mod, type_, name=name)
        for arg, name in zip(func.args, self.args):
            arg.name = str(name)
        return func


def prototype(name, *args):
    return Prototype(Symbol(name), [Symbol(arg) for arg in args])


class Definition(ASTNode):

    def __init__(self, prototype, body):
        self.prototype = prototype
        self.body = body

    def __repr__(self):
        return f'{{def {self.prototype!r} {self.body!r}}}'

    def __str__(self):
        return str(self.prototype)

    def codegen(self, gen, mod, loc):
        func = self.prototype.codegen(gen, mod, loc)
        blk = func.append_basic_block('entry')
        bld = ir.IRBuilder(blk)

        names = dict(loc, **{arg.name: arg for arg in func.args})
        retval = self.body.codegen(gen, bld, names)
        bld.ret(retval)
        return func


class ExprWrapper(Definition):

    def __init__(self, body):
        super(ExprWrapper, self).__init__(Prototype(None, []), body)

    def __repr__(self):
        return f'{{wrp {self.body!r}}}'
