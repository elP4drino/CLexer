from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

from llvmlite import ir

int32 = ir.IntType(32)
float32 = ir.FloatType()

# Definición global
class ASTNode(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass

class Visitor(ABC):
    @abstractmethod
    def visit_program(self, node: Program) -> None:
        pass
    @abstractmethod
    def visit_for_statement(self, node: ForStatement) -> None:
        pass
    @abstractmethod
    def visit_if_statement(self, node: IfStatement) -> None:
        pass
    @abstractmethod
    def visit_if_else_statement(self, node: IfElseStatement) -> None:
        pass
    @abstractmethod
    def visit_while_statement(self, node: WhileStatement) -> None:
        pass
    @abstractmethod
    def visit_boolean_op(self, node: BooleanOp) -> None:
        pass
    @abstractmethod
    def visit_relational_op(self, node: RelationalOp) -> None:
        pass
    @abstractmethod
    def visit_binary_op(self, node: BinaryOp) -> None:
        pass
    @abstractmethod
    def visit_assignment(self, node: Assignment) -> None:
        pass
    @abstractmethod
    def visit_declaration(self, node: Declaration) -> None:
        pass
    @abstractmethod
    def visit_literal(self, node: Literal) -> None:
        pass

class Program(ASTNode):
    def __init__(self, declarations: list, statements: list) -> None:
        self.declarations = declarations
        self.statements = statements
    
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_program(self)

class ForStatement(ASTNode):
    def __init__(self, declaration: ASTNode, expression: ASTNode, assignment: ASTNode, statements: list) -> None:
        self.declaration = declaration
        self.expression = expression
        self.assignment = assignment
        self.statements = statements

    def accept(self, visitor: Visitor):
        visitor.visit_for_statement(self)

class IfStatement(ASTNode):
    def __init__(self, expression: ASTNode, statements: list) -> None:
        self.expression = expression
        self.statements = statements

    def accept(self, visitor: Visitor):
        visitor.visit_if_statement(self)

class IfElseStatement(ASTNode):
    def __init__(self, expression: ASTNode, then_statements: list, otherwise_statements: list) -> None:
        self.expression = expression
        self.then_statements = then_statements
        self.otherwise_statements = otherwise_statements

    def accept(self, visitor: Visitor):
        visitor.visit_if_else_statement(self)

class WhileStatement(ASTNode):
    def __init__(self, expression: ASTNode, statements: list) -> None:
        self.expression = expression
        self.statements = statements

    def accept(self, visitor: Visitor):
        visitor.visit_while_statement(self)

class BooleanOp(ASTNode):
    def __init__(self, op: str, lhs: ASTNode, rhs: ASTNode) -> None:
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def accept(self, visitor: Visitor):
        visitor.visit_relational_op(self)

class RelationalOp(ASTNode):
    def __init__(self, op: str, lhs: ASTNode, rhs: ASTNode) -> None:
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def accept(self, visitor: Visitor):
        visitor.visit_relational_op(self)

class BinaryOp(ASTNode):
    def __init__(self, op: str, lhs: ASTNode, rhs: ASTNode) -> None:
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def accept(self, visitor: Visitor):
        visitor.visit_binary_op(self)

class Assignment(ASTNode):
    def __init__(self, id: str, value: ASTNode) -> None:
        self.id = id
        self.value = value

    def accept(self, visitor: Visitor):
        visitor.visit_assignment(self)

class Declaration(ASTNode):
    def __init__(self, type: str, id: str, value: ASTNode) -> None:
        self.type = type
        self.id = id
        self.value = value

    def accept(self, visitor: Visitor):
        visitor.visit_declaration(self)

class Literal(ASTNode):
    def __init__(self, value: Any, type: str) -> None:
        self.value = value
        self.type = type

    def accept(self, visitor: Visitor):
        visitor.visit_literal(self)

class IR(Visitor):
    def __init__(self):
        self.module = ir.Module()
        self.function = ir.Function(self.module, ir.FunctionType(ir.VoidType(), []), name="main")
        self.block = self.function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(self.block)
        self.definitions = {}
        self.stack = []

    def visit_program(self, node: Program) -> None:
        if node.declarations:
            for declaration in node.declarations:
                declaration.accept(self)

        if node.statements:
            for statement in node.statements:
                statement.accept(self)

    def visit_for_statement(self, node: ForStatement) -> None:
        # Declaration is taken as an assignment, therefore, the variable must be initialized first
        node.declaration.accept(self)
        node.expression.accept(self)
        condition = self.stack.pop()

        forHead = self.function.append_basic_block('for-head')
        forBody = self.function.append_basic_block('for-body')
        forExit = self.function.append_basic_block('for-exit')

        self.builder.branch(forHead)
        self.builder.position_at_start(forHead)
        self.builder.cbranch(
            condition,
            forBody, forExit
        )
        
        # If there are more than one statement, add the assignment to the statements
        if isinstance(node.statements[0], list):
            node.statements = node.statements[0] # Flatten the list
            node.statements.append(node.assignment) # Append the assingment to the end of the list

        # Start the loop body
        self.builder.position_at_start(forBody)
        for statement in node.statements:
            statement.accept(self)

        self.builder.branch(forHead)
        self.builder.position_at_start(forExit)

    def visit_if_statement(self, node: IfStatement) -> None:
        node.expression.accept(self)
        condition = self.stack.pop()
        with self.builder.if_then(condition):
            # Emmit instructions for when the predicate is true
            if isinstance(node.statements, list):
                for statement in node.statements:
                    statement.accept(self)
            else:
                statement.accept(self)
    
    def visit_if_else_statement(self, node: IfElseStatement) -> None:
        node.expression.accept(self)
        condition = self.stack.pop()
        with self.builder.if_else(condition) as (then, otherwise):
            # Emmit instructions for when the predicate is true
            with then:
                if isinstance(node.then_statements, list):
                    for statement in node.then_statements:
                        statement.accept(self)
                else:
                    statement.accept(self)
            with otherwise:
                if isinstance(node.otherwise_statements, list):
                    for statement in node.otherwise_statements:
                        statement.accept(self)
                else:
                    statement.accept(self)

    def visit_while_statement(self, node: WhileStatement) -> None:
        node.expression.accept(self)
        condition = self.stack.pop()
        whileHead = self.function.append_basic_block('while-head')
        whileBody = self.function.append_basic_block('while-body')
        whileExit = self.function.append_basic_block('while-exit')

        self.builder.branch(whileHead)
        self.builder.position_at_start(whileHead)
        self.builder.cbranch(
            condition,
            whileBody, whileExit
        )
        
        if isinstance(node.statements[0], list):
            # Flatten the list
            node.statements = node.statements[0]

        # Start the loop body
        self.builder.position_at_start(whileBody)
        for statement in node.statements:
            statement.accept(self)

        self.builder.branch(whileHead)
        self.builder.position_at_start(whileExit)

    def visit_boolean_op(self, node: BooleanOp) -> None:
        pass# Start the loop body

    def visit_relational_op(self, node: RelationalOp) -> None:
        node.lhs.accept(self)
        node.rhs.accept(self)
        lhs = self.stack.pop()
        rhs = self.stack.pop()

        self.stack.append(self.builder.icmp_signed(node.op, lhs, rhs))

    def visit_binary_op(self, node: BinaryOp) -> None:
        node.lhs.accept(self)
        node.rhs.accept(self)
        lhs = self.stack.pop()
        rhs = self.stack.pop()

        # Check wheter the value has been allocated or not and load its value
        if isinstance(lhs, ir.instructions.AllocaInstr):
            lhs = self.builder.load(lhs, name=lhs.name)
        elif isinstance(rhs, ir.instructions.AllocaInstr):
            rhs = self.builder.load(rhs, name=rhs.name)

        if node.op == '+':
            self.stack.append(self.builder.add(lhs, rhs))
        elif node.op == '-':
            self.stack.append(self.builder.sub(lhs, rhs))
        elif node.op == '*':
            self.stack.append(self.builder.mul(lhs, rhs))
        elif node.op == '/':
            self.stack.append(self.builder.sdiv(lhs, rhs))

    def visit_assignment(self, node: Assignment) -> None:
        if node.id not in self.definitions:
            raise # Variable is not defined, raise an error
        
        node.value.accept(self)
        value = self.stack.pop()
        variable = self.definitions[node.id]
        data_type = variable[1]
        allocation = variable[0]

        if data_type == 'int':
            self.builder.store(ir.Constant(int32, value), allocation)
        elif data_type == 'float':
            self.builder.store(ir.Constant(float32, value), allocation)

    def allocate(self, type, id):
        allocation = None
        if type == 'int':
            allocation = self.builder.alloca(int32, name=id)
        elif type == 'float':
            allocation = self.builder.alloca(float32, name=id)
        
        self.definitions[id] = (allocation, type)


    def visit_declaration(self, node: Declaration) -> None:
        if node.id in self.definitions:
            raise # Re-defined variable, raise an error
        
        if not node.value: # Just the definition
            self.allocate(node.type, node.id)
        else: # Variable is defined with a value
            self.allocate(node.type, node.id)
            definition = self.definitions[node.id]
            allocation = definition[0]
            type = definition[1]
            node.value.accept(self)
            value = self.stack.pop()
            if type == 'int':
                self.builder.store(ir.Constant(int32, value), allocation)
            elif type == 'float':
                self.builder.store(ir.Constant(float32, value), allocation)

    def visit_literal(self, node: Literal) -> None:
        if node.type == 'INT':
            new_value = int32(node.value)
            self.stack.append(new_value)
        elif node.type == 'FLOAT':
            new_value = float32(node.value)
            self.stack.append(new_value)
        else: # Visit a literal that is an identifier, e.g. x = (x <- literal) + 1
            definition = self.definitions[node.value]
            variable = definition[0]
            self.stack.append(variable)