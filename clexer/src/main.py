from src.compiler import Compiler
from src.ir import IR

compiler = Compiler()
compiler.build_parser()


ast = compiler.get_AST('int main () { for (int x = 5; x < 5; x = x + 1) x = 5; }')
ir = IR()
ast.accept(ir)
print(ir.module)