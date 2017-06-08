import llvmlite.ir as ir
import llvmlite.binding as llvm

from pyka.ast import Definition


llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()


class CodeGen:

    def __init__(self):
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_mod = llvm.parse_assembly('')
        self.engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
        self.module = ir.Module(name='Kaleidoscope')

        self._counter = -1
        self._names = {}

    def name(self):
        self._counter += 1
        return f'//anonymous_{self._counter}'

    def generate(self, node):
        return node.codegen(self, self.module, self._names)

    def register(self, name, value):
        self._names[str(name)] = value

    def function(self, name):
        for func in self.module.functions:
            if func.name == str(name):
                return func
