import click

from pyka.codegen import CodeGen
from pyka.parser import KaleidoscopeParser, KaleidoscopeSemantics


@click.command()
def main():
    parser = KaleidoscopeParser(
        parseinfo=True,
        semantics=KaleidoscopeSemantics()
    )
    nodes = []

    while True:
        inp = input('> ')
        last_node = parser.parse(inp, 'toplevel')
        print(repr(last_node))

        gen = CodeGen()
        for node in nodes:
            gen.generate(node)
        func = gen.generate(last_node)

        print(str(gen.module))

        nodes.append(last_node)


if __name__ == '__main__':
    main()
