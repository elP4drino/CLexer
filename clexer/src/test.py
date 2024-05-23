from llvmlite import ir

# Creamos un nuevo módulo
module = ir.Module()

# Creamos una nueva función en el módulo
function_type = ir.FunctionType(ir.VoidType(), [])
function = ir.Function(module, ir.FunctionType(ir.VoidType(), []), name="main")

# Creamos un bloque de entrada en la función
entry_block = function.append_basic_block(name="entry")
loop_block = function.append_basic_block(name="loop")
exit_block = function.append_basic_block(name="exit")

# Creamos un IRBuilder para el bloque de entrada
builder = ir.IRBuilder(entry_block)

# Creamos una variable de contador y la inicializamos a 0
counter = builder.alloca(ir.IntType(32), name="counter")
builder.store(ir.Constant(ir.IntType(32), 0), counter)

# Creamos la condición de bucle
cond = builder.icmp_unsigned('<', builder.load(counter), ir.Constant(ir.IntType(32), 10))

# Insertamos una rama condicional para comenzar el bucle o salir
builder.cbranch(cond, loop_block, exit_block)

# Construimos el bloque del bucle
builder = ir.IRBuilder(loop_block)
# Aquí colocarías las instrucciones dentro del bucle

# Incrementamos el contador
old_counter = builder.load(counter)
new_counter = builder.add(old_counter, ir.Constant(ir.IntType(32), 1))
builder.store(new_counter, counter)

# Saltamos al bloque de salida
builder.branch(entry_block)

# Construimos el bloque de salida
builder = ir.IRBuilder(exit_block)

# Retornamos desde la función
builder.ret_void()

# Imprimimos el IR generado
print(module)
