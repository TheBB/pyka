import click

from pyka.ast import ExprWrapper
from pyka.codegen import CodeGen
from pyka.parser import KaleidoscopeParser, KaleidoscopeSemantics


@click.command()
def main():
    parser = KaleidoscopeParser(
        parseinfo=True,
        semantics=KaleidoscopeSemantics()
    )
    nodes = []
    gen = CodeGen()

    while True:
        inp = input('> ')
        node = parser.parse(inp, 'toplevel')
        func = gen.generate(node)
        if isinstance(node, ExprWrapper):
            print(gen.run_wrapper(func.name))


if __name__ == '__main__':
    main()
