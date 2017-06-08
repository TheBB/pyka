from pyka.ast import Symbol, Number, BinOp, Call, Prototype, Definition, ExprWrapper
from pyka.gen_grammar import KaleidoscopeSemantics as GenSemantics, KaleidoscopeParser


class KaleidoscopeSemantics(GenSemantics):

    def toplevel(self, arg):
        if isinstance(arg, (Prototype, Definition)):
            return arg
        return ExprWrapper(arg)

    def definition(self, args):
        prototype, body = args
        return Definition(prototype, body)

    def arith(self, args):
        head, tail = args
        for op, rhs in tail:
            head = BinOp(op, head, rhs)
        return head

    term = arith

    def trailer_expr(self, args):
        head, tail = args
        for type_, contents, *_ in tail:
            if type_ == '(':
                head = Call(head, contents)
        return head

    def prototype(self, args):
        head, tail = args
        return Prototype(head, tail)

    def symbol(self, arg):
        return Symbol(arg)

    def number(self, arg):
        return Number(float(arg))
