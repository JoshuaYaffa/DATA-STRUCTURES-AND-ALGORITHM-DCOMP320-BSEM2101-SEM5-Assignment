"""
Math Expression Evaluator
=========================

A stack-based evaluator for mathematical expressions.

Reads expressions from data/input.txt, evaluates each one using a
stack-based approach (shunting-yard algorithm + postfix evaluation),
and writes results to data/output.txt.

Supported operators:  + - * / ( )
Supports multi-digit integers and whitespace-optional input.
"""

import os


# ===============================================================
# 1. STACK
# ===============================================================
class Stack:
    """A Last-In-First-Out (LIFO) stack built on top of a Python list."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"


# ===============================================================
# 2. TOKENIZER
# ===============================================================
def tokenize(expression):
    """Convert an expression string into a list of string tokens."""
    tokens = []
    i = 0
    n = len(expression)

    while i < n:
        c = expression[i]

        if c.isspace():
            i += 1
            continue

        if c.isdigit():
            start = i
            while i < n and expression[i].isdigit():
                i += 1
            tokens.append(expression[start:i])
            continue

        if c in "+-*/()":
            tokens.append(c)
            i += 1
            continue

        raise ValueError(f"Unexpected character: {c!r} at position {i}")

    return tokens


# ===============================================================
# 3. SHUNTING-YARD
# ===============================================================
PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
}


def infix_to_postfix(tokens):
    """Convert infix tokens to postfix (RPN) using shunting-yard."""
    output = []
    operators = Stack()

    for token in tokens:
        if token.isdigit():
            output.append(token)

        elif token in PRECEDENCE:
            while (not operators.is_empty()
                   and operators.peek() in PRECEDENCE
                   and PRECEDENCE[operators.peek()] >= PRECEDENCE[token]):
                output.append(operators.pop())
            operators.push(token)

        elif token == '(':
            operators.push(token)

        elif token == ')':
            while not operators.is_empty() and operators.peek() != '(':
                output.append(operators.pop())
            if operators.is_empty():
                raise ValueError("Mismatched parentheses: missing '('")
            operators.pop()

        else:
            raise ValueError(f"Unknown token: {token!r}")

    while not operators.is_empty():
        top = operators.pop()
        if top == '(':
            raise ValueError("Mismatched parentheses: missing ')'")
        output.append(top)

    return output


# ===============================================================
# 4. POSTFIX EVALUATOR
# ===============================================================
def eval_postfix(postfix_tokens):
    """Evaluate a postfix (RPN) expression using a stack."""
    stack = Stack()

    for token in postfix_tokens:
        if token.isdigit():
            stack.push(int(token))
        else:
            if stack.size() < 2:
                raise ValueError(f"Invalid expression near {token!r}")
            right = stack.pop()
            left = stack.pop()

            if token == '+':
                result = left + right
            elif token == '-':
                result = left - right
            elif token == '*':
                result = left * right
            elif token == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                result = left // right
            else:
                raise ValueError(f"Unknown operator: {token!r}")

            stack.push(result)

    if stack.size() != 1:
        raise ValueError("Invalid expression: leftover operands")

    return stack.pop()


# ===============================================================
# 5. HIGH-LEVEL EVALUATE
# ===============================================================
def evaluate(expression):
    """Tokenize -> infix-to-postfix -> evaluate. Returns an integer."""
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("Empty expression")
    postfix = infix_to_postfix(tokens)
    return eval_postfix(postfix)


# ===============================================================
# 6. FILE I/O
# ===============================================================
def is_separator(line):
    """Return True if the line is a separator (dashes/spaces)."""
    stripped = line.strip()
    if not stripped:
        return False
    return all(ch in '- \t' for ch in stripped) and '-' in stripped


def process_file(input_path, output_path):
    """
    Read expressions from input_path, evaluate each one,
    and write results to output_path — preserving separators.

    Writes to a temporary file first, then atomically replaces the
    destination. This avoids "Permission denied" errors when the
    destination file is open in an editor (e.g. PyCharm or VS Code).
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # ---- Read input ----
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # ---- Evaluate each line ----
    results = []
    for line in lines:
        raw = line.rstrip('\n')

        if raw.strip() == '':
            results.append('')
            continue

        if is_separator(raw):
            results.append(raw)
            continue

        try:
            value = evaluate(raw)
            results.append(str(value))
        except Exception as e:
            results.append(f"ERROR: {e}")

    # ---- Write to a temporary file first ----
    tmp_path = output_path + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8') as outfile:
        for line in results:
            outfile.write(line + '\n')

    # ---- Replace the destination atomically ----
    os.replace(tmp_path, output_path)


# ===============================================================
# 7. MAIN
# ===============================================================
def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)

    input_path = os.path.join(project_root, 'data', 'input.txt')
    output_path = os.path.join(project_root, 'data', 'output.txt')

    print(f"Reading:  {input_path}")
    print(f"Writing:  {output_path}")
    process_file(input_path, output_path)
    print("Done.")


# ===============================================================
# MANUAL TESTS  (run with: py src\main.py)
# ===============================================================
if __name__ == "__main__":
    print("=== Stack ===")
    s = Stack()
    print("Empty?     ", s.is_empty())
    s.push(1); s.push(2); s.push(3)
    print("After push:", s)
    print("Peek:      ", s.peek())
    print("Pop:       ", s.pop())
    print("Size:      ", s.size())

    print("\n=== Tokenizer ===")
    for expr in ["3 + 5 * 2", "(8 / 4) + 7 * 2",
                 "10 - (2 + 3) * 4", "10-(2+3)*4", "  42  "]:
        print(f"{expr!r:25} -> {tokenize(expr)}")

    print("\n=== Infix -> Postfix ===")
    for expr in ["3 + 5 * 2", "(8 / 4) + 7 * 2", "10 - (2 + 3) * 4"]:
        print(f"{expr!r:25} -> {infix_to_postfix(tokenize(expr))}")

    print("\n=== Evaluate ===")
    for expr in ["3 + 5 * 2", "(8 / 4) + 7 * 2", "10 - (2 + 3) * 4"]:
        print(f"{expr!r:25} = {evaluate(expr)}")

    print("\n=== Full pipeline (file I/O) ===")
    main()