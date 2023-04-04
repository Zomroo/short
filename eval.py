import ast
import traceback


def eval_expr(expr):
    """
    Evaluate a Python expression.

    Args:
        expr (str): The expression to evaluate.

    Returns:
        The result of the evaluation.
    """
    try:
        # Use `ast.literal_eval` for safety
        return ast.literal_eval(expr)
    except Exception:
        # If there's a syntax error, evaluate the expression as a statement
        try:
            exec(expr)
        except Exception as e:
            return str(e)


def eval_code(code):
    """
    Evaluate a block of Python code.

    Args:
        code (str): The code to evaluate.

    Returns:
        The result of the evaluation.
    """
    try:
        # Compile the code
        compiled = compile(code, '<string>', 'exec')
        # Execute the code
        exec(compiled)
    except Exception:
        # If there's a syntax error, print the traceback
        return traceback.format_exc()


if __name__ == '__main__':
    while True:
        expr = input('> ')
        print(eval_expr(expr))
