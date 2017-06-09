import ctypes as ct
import llvmlite.ir as ir
import llvmlite.binding as llvm

from pyka.ast import Definition, Prototype, prototype, Symbol
import pyka.runtime as runtime


llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()
llvm.load_library_permanently('/lib/libm.so.6')


class CodeGen:

    def __init__(self):
        self.module = ir.Module(name='Kaleidoscope')

        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_mod = llvm.parse_assembly('')
        self.engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

        self._prototypes = {
            'sin': prototype('sin', 'x'),
            'cos': prototype('cos', 'x'),
            'sqrt': prototype('sqrt', 'x'),
        }
        self._runtime = []

        for func in runtime.__all__:
            wrap = runtime.Wrap(getattr(runtime, func))
            self._runtime.append(wrap)
            llvm.add_symbol(str(wrap), wrap.addr)
            self._prototypes[str(wrap)] = wrap.prototype

    def name(self):
        return '//anonymous'

    def generate(self, node):
        if isinstance(node, Prototype):
            self._prototypes[str(node)] = node
        elif isinstance(node, Definition):
            self._prototypes[str(node)] = node.prototype
        val = node.codegen(self, self.module, {})
        if isinstance(node, Definition):
            self.compile()
            self.module = ir.Module(name='Kaleidoscope')
        return val

    def function(self, name):
        for func in self.module.functions:
            if func.name == name:
                return func
        return self._prototypes[name].codegen(self, self.module, {})

    def compile(self):
        print(str(self.module))
        refmod = llvm.parse_assembly(str(self.module))
        refmod.verify()

        pmb = llvm.create_pass_manager_builder()
        pmb.opt_level = 2
        pm = llvm.create_module_pass_manager()
        pmb.populate(pm)
        pm.run(refmod)

        self.engine.add_module(refmod)
        self.engine.finalize_object()

    def run_wrapper(self, name):
        addr = self.engine.get_function_address(name)
        func = ct.CFUNCTYPE(ct.c_double)(addr)
        return float(func())
