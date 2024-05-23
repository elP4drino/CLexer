from src.cparser import CParser

class Compiler:
    def __init__(self) -> None:
        self.parser = CParser()

    def build_parser(self) -> None:
        self.parser.build()

    def get_AST(self, t_string) -> None:
        ast = self.parser.parse(t_string)
        
        return ast