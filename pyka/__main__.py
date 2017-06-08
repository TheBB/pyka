import click

from pyka.parser import KaleidoscopeParser, KaleidoscopeSemantics


@click.command()
def main():
    parser = KaleidoscopeParser(
        parseinfo=True,
        semantics=KaleidoscopeSemantics()
    )

    while True:
        inp = input('> ')
        ast = parser.parse(inp, 'toplevel')
        print(ast)


if __name__ == '__main__':
    main()
