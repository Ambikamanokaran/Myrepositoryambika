"""calculator.py

A simple and safe command-line calculator.

Features:
- Evaluate arithmetic expressions entered by the user (supports +, -, *,, /, %, **, parentheses)
- Supports math functions: sin, cos, tan, sqrt, log, log10, exp, floor, ceil, factorial
- Prevents arbitrary code execution by parsing expressions with ast and whitelisting nodes
- Usage:
    python calculator.py           # interactive REPL
    python calculator.py "2+2*3"  # evaluate single expression and exit

"""
import ast
import operator as op
import math
import sys

# Allowed binary operators
BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators
UNARY_OPS = {
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

# Whitelisted math functions
SAFE_FUNCS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'log': math.log,       # natural log: log(x, base) supported if 2 args
    'log10': math.log10,
    'exp': math.exp,
    'floor': math.floor,
    'ceil': math.ceil,
    'factorial': math.factorial,
    'abs': abs,
    'round': round,
}

# Allowed names/constants
SAFE_NAMES = {
    'pi': math.pi,
    'e': math.e,
}


class CalcEvaluator(ast.NodeVisitor):
    """Evaluate a math expression AST safely."""

    def visit(self, node):
        # Override to raise on disallowed nodes early
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor is None:
            raise ValueError(f"Unsupported expression: {node.__class__.__name__}")
        return visitor(node)

    def visit_Module(self, node):
        if len(node.body) != 1 or not isinstance(node.body[0], ast.Expr):
            raise ValueError("Only single expressions are allowed")
        return self.visit(node.body[0].value)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type in BIN_OPS:
            try:
                return BIN_OPS[op_type](left, right)
            except Exception as e:
                raise ValueError(f"Error during binary operation: {e}")
        raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in UNARY_OPS:
            return UNARY_OPS[op_type](operand)
        raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

    def visit_Num(self, node):
        return node.n

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    def visit_Name(self, node):
        if node.id in SAFE_NAMES:
            return SAFE_NAMES[node.id]
        raise ValueError(f"Unknown identifier: {node.id}")

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls allowed")
        func_name = node.func.id
        if func_name not in SAFE_FUNCS:
            raise ValueError(f"Function not allowed: {func_name}")
        func = SAFE_FUNCS[func_name]
        args = [self.visit(a) for a in node.args]
        try:
            return func(*args)
        except Exception as e:
            raise ValueError(f"Error in function call {func_name}: {e}")

    # Disallow attribute access, subscripting, comprehensions, etc.
    def generic_visit(self, node):
        raise ValueError(f"Unsupported expression element: {node.__class__.__name__}")


def safe_eval(expr: str):
    """Safely evaluate a math expression string and return a number.

    Raises ValueError on invalid or unsafe expressions.
    """
    try:
        tree = ast.parse(expr, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}")
    evaluator = CalcEvaluator()
    return evaluator.visit(tree)


def repl():
    print("Welcome to calculator.py — safe arithmetic REPL")
    print("Type 'help' for usage, 'quit' or 'exit' to leave.")
    while True:
        try:
            s = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not s:
            continue
        if s.lower() in ('quit', 'exit'):
            break
        if s.lower() in ('help', '?'):
            print_help()
            continue
        try:
            result = safe_eval(s)
            print(result)
        except Exception as e:
            print(f"Error: {e}")


def print_help():
    print("Enter arithmetic expressions using +, -, *, /, %, ** and parentheses.")
    print("Allowed functions: " + ', '.join(sorted(SAFE_FUNCS.keys())))
    print("Constants: " + ', '.join(f"{k}={v}" for k, v in SAFE_NAMES.items()))
    print("Examples:")
    print("  2 + 2 * 3")
    print("  sqrt(2) + sin(pi/4)")
    print("  factorial(5)")


def main():
    if len(sys.argv) > 1:
        expr = ' '.join(sys.argv[1:])
        try:
            print(safe_eval(expr))
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(2)
        return
    repl()


if __name__ == '__main__':
    main()
