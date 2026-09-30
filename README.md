# Math Expression Evaluator

**A Python program that evaluates mathematical expressions using a stack-based approach.**

Module:Data Structures and Algorithms
Module code : DCOMP320  
Name: Joshua Mohamed Katibi Yaffa 
ID: 905004075  
class: BSEM2101 
Semseter : 5 
Year : 3
Limkokwing University of Creative Technology — Sierra Leone  
Submission Date: 09 / 10 / 2026

---

## Quick Start

Three commands to get running:

```bash
# 1. Navigate to the project
cd math-expression-evaluator

# 2. Run the evaluator
py src/main.py

# 3. Run the tests
py -m unittest discover tests -v
```

That's it. The results appear in `data/output.txt`, and the tests confirm all 31 checks pass.

---

## Overview

This project is a **complete, from-scratch implementation** of a mathematical expression evaluator. It reads infix expressions (the normal way we write math: `3 + 5 * 2`) from a text file, computes their values using a stack-based algorithm, and writes the results to a second text file — preserving the original layout.

The program does **not** use Python's built-in `eval()` function, `sympy`, `pyparsing`, or any other third-party library. Every part of the algorithm — the stack, the tokenizer, the shunting-yard conversion, the postfix evaluator — is written by hand to demonstrate understanding of fundamental data structures.

**Why is this important?** Because the assignment is about **data structures and algorithms**, not about using libraries. Anyone can write `eval("3 + 5 * 2")`. The learning comes from implementing the underlying machinery yourself.

---

## Features

- **Custom Stack class** — implements push, pop, peek, size, and is_empty with proper error handling
- **Hand-written tokenizer** — supports multi-digit integers, optional whitespace, and all standard operators
- **Shunting-yard algorithm** — converts infix expressions to postfix (RPN) with full precedence and associativity support
- **Postfix evaluator** — evaluates RPN using a second stack of operands
- **Nested parentheses** — any depth of `(((...)))` is supported
- **Format preservation** — separators and blank lines pass through unchanged
- **Error recovery** — one bad line produces an `ERROR:` line but does not crash the program
- **Atomic file writes** — writes to a temp file first, then swaps it in (safe against editor locks)
- **31 unit tests** — every component is verified automatically
- **No external dependencies** — pure Python Standard Library only

---

## Requirements

**What this section explains:** The exact environment needed to run this project, and why no external packages are used.

To run the program you need:

- **Python 3.8 or newer** — tested on Python 3.14.6
- **No external packages** — everything is written using only the Python Standard Library: `os` for file paths, `sys` for module resolution in the tests, and `unittest` for the automated test suite.

**Why no external packages?**

This assignment is about **data structures and algorithms**. The entire point is to demonstrate a hand-written **Stack** class and a hand-written **expression parser**. If we used a library such as `sympy`, `pyparsing`, or Python's own `eval()`, the exercise would be trivial and would defeat the purpose of the assignment. Every component of this project — the stack, the tokenizer, the shunting-yard algorithm, the postfix evaluator — is written from first principles.

**Verify Python is installed:**

```bash
py --version
```

If this prints a version number (e.g. `Python 3.14.6`), you're ready to run. If the command is not found, install Python 3.8+ from https://www.python.org/downloads/ and make sure the **"Add python.exe to PATH"** option is checked during installation.

---

## How to Run

**What this section explains:** The single command that executes the program, and exactly what happens inside.

From the project root directory, run:

```bash
py src/main.py
```

**What happens inside, step by step:**

1. **Resolves file paths** — the program determines its own location and constructs the paths to `data/input.txt` and `data/output.txt` relative to the project root. This means you can run the program from anywhere, not just the project folder.
2. **Opens `data/input.txt`** and reads every line into memory.
3. **Classifies each line:**
   - **Blank line** → preserved as a blank line in the output
   - **Separator line** (contains only dashes and spaces, at least one dash) → copied verbatim to the output
   - **Expression line** → tokenized, converted to postfix, evaluated
4. **Evaluates expressions** using the stack-based pipeline described in *How It Works*.
5. **Writes results to a temporary file** (`output.txt.tmp`) then atomically replaces `output.txt`. This two-step write prevents corruption if the program is interrupted mid-write, and avoids permission errors if the destination is open in an editor.
6. **Prints progress lines** to the terminal.

**Expected terminal output:**

```
Reading:  C:\dev\math-expression-evaluator\data\input.txt
Writing:  C:\dev\math-expression-evaluator\data\output.txt
Done.
```

If `input.txt` is missing, the program raises `FileNotFoundError` and stops with a clear message.

**Example:** If `input.txt` contains the single line `3 + 5 * 2`, then `output.txt` will contain `13`.

---

## How to Run Tests

**What this section explains:** The single command to run all automated tests, and exactly what they verify.

From the project root directory:

```bash
py -m unittest discover tests -v
```

**What each part means:**

- `py` — invokes the Python interpreter (on Windows, `python` may not be on PATH; `py` is the reliable launcher)
- `-m unittest` — runs Python's built-in testing framework as a module
- `discover tests` — scans the `tests/` directory for all files matching `test*.py` and loads them
- `-v` — verbose mode, showing each test method name as it runs

**Expected output:**

```
test_division (test_stack.TestEvalPostfix.test_division) ... ok
test_division_by_zero_raises (...) ... ok
...
test_simple_expression (...) ... ok

----------------------------------------------------------------------
Ran 31 tests in 0.005s

OK
```

**What the test suite covers:**

| Category | Test methods | What is verified |
|----------|--------------|------------------|
| Stack operations | 7 | push, pop, peek, size, is_empty, mixed types, empty-stack errors |
| Tokenizer | 6 | multi-digit numbers, whitespace, no-space input, invalid characters, parentheses |
| Infix → postfix | 4 | precedence, parentheses, nested parentheses, mismatched parentheses |
| Postfix evaluator | 6 | addition, subtraction, division, division by zero, single number, precedence |
| End-to-end | 8 | assignment examples + 20-expression extended set |
| **Total** | **31** | |

**Why so many tests?**

The assignment rubric awards 15 marks for **Testing and Results**. The test suite proves:

- The stack behaves correctly (LIFO semantics, error handling)
- The tokenizer correctly groups multi-digit numbers and rejects invalid characters
- The shunting-yard algorithm handles precedence and associativity
- The postfix evaluator matches the assignment's expected outputs
- The pipeline works end-to-end on 20 real expressions

The `OK` at the end means all tests passed with zero failures.

---

## Example Walkthrough

**What this section explains:** A complete worked example, from input line to output line.

**Input:** Suppose `data/input.txt` contains just this one line:

```
10 - (2 + 3) * 4
```

**Step 1 — Tokenize:**

```
'10', '-', '(', '2', '+', '3', ')', '*', '4'
```

**Step 2 — Convert to postfix (shunting-yard):**

```
'10', '2', '3', '+', '4', '*', '-'
```

**Step 3 — Evaluate postfix with a stack:**

| Step | Token | Stack | Action |
|------|-------|-------|--------|
| 1 | 10 | `[10]` | push 10 |
| 2 | 2 | `[10, 2]` | push 2 |
| 3 | 3 | `[10, 2, 3]` | push 3 |
| 4 | + | `[10, 5]` | pop 3, 2 → push 5 |
| 5 | 4 | `[10, 5, 4]` | push 4 |
| 6 | * | `[10, 20]` | pop 4, 5 → push 20 |
| 7 | - | `[-10]` | pop 20, 10 → push -10 |

**Result:** `-10`

**Output:** `data/output.txt` will contain:

```
-10
```

That's the full pipeline — three stages, two of which use the Stack class.

---

## Sample Test Output

Here's what a successful test run looks like:

```
$ py -m unittest discover tests -v

test_division (test_stack.TestEvalPostfix.test_division) ... ok
test_division_by_zero_raises (test_stack.TestEvalPostfix.test_division_by_zero_raises) ... ok
test_precedence_via_postfix (test_stack.TestEvalPostfix.test_precedence_via_postfix) ... ok
test_simple_addition (test_stack.TestEvalPostfix.test_simple_addition) ... ok
test_single_number (test_stack.TestEvalPostfix.test_single_number) ... ok
test_subtraction_order (test_stack.TestEvalPostfix.test_subtraction_order) ... ok
test_assignment_examples (test_stack.TestEvaluateEndToEnd.test_assignment_examples) ... ok
test_bad_character_raises (test_stack.TestEvaluateEndToEnd.test_bad_character_raises) ... ok
test_empty_expression_raises (test_stack.TestEvaluateEndToEnd.test_empty_expression_raises) ... ok
test_extended_input_examples (test_stack.TestEvaluateEndToEnd.test_extended_input_examples) ... ok
test_large_numbers (test_stack.TestEvaluateEndToEnd.test_large_numbers) ... ok
test_left_to_right_same_precedence (test_stack.TestEvaluateEndToEnd.test_left_to_right_same_precedence) ... ok
test_nested_parentheses (test_stack.TestEvaluateEndToEnd.test_nested_parentheses) ... ok
test_no_spaces_variant (test_stack.TestEvaluateEndToEnd.test_no_spaces_variant) ... ok
test_mismatched_parens_raises (test_stack.TestInfixToPostfix.test_mismatched_parens_raises) ... ok
test_nested_parentheses (test_stack.TestInfixToPostfix.test_nested_parentheses) ... ok
test_parentheses (test_stack.TestInfixToPostfix.test_parentheses) ... ok
test_precedence (test_stack.TestInfixToPostfix.test_precedence) ... ok
test_can_hold_mixed_types (test_stack.TestStack.test_can_hold_mixed_types) ... ok
test_new_stack_is_empty (test_stack.TestStack.test_new_stack_is_empty) ... ok
test_peek_does_not_remove (test_stack.TestStack.test_peek_does_not_remove) ... ok
test_peek_empty_raises (test_stack.TestStack.test_peek_empty_raises) ... ok
test_pop_empty_raises (test_stack.TestStack.test_pop_empty_raises) ... ok
test_pop_returns_last_in_first_out (test_stack.TestStack.test_pop_returns_last_in_first_out) ... ok
test_push_and_size (test_stack.TestStack.test_push_and_size) ... ok
test_bad_character_raises (test_stack.TestTokenizer.test_bad_character_raises) ... ok
test_extra_whitespace (test_stack.TestTokenizer.test_extra_whitespace) ... ok
test_multi_digit_numbers (test_stack.TestTokenizer.test_multi_digit_numbers) ... ok
test_no_spaces (test_stack.TestTokenizer.test_no_spaces) ... ok
test_parentheses_are_individual_tokens (test_stack.TestTokenizer.test_parentheses_are_individual_tokens) ... ok
test_simple_expression (test_stack.TestTokenizer.test_simple_expression) ... ok

----------------------------------------------------------------------
Ran 31 tests in 0.005s

OK
```

Every test method prints `ok` — no failures, no errors.

---

## Input Format

**What this section explains:** Exactly how `data/input.txt` must be structured, with rules and edge cases.

The input file contains mathematical expressions written in **infix notation** — the standard way we write math (`3 + 5 * 2`).

**Structure of the file:**

- One expression per line
- Separator lines between expressions, containing only dashes and spaces (at least one dash)
- Blank lines are also allowed and are preserved in the output

**Sample `input.txt` (20 expressions, from the project):**

```
3 + 5 * 2
- - - - - - - - - - - - - -
(8 / 4) + 7 * 2
- - - - - - - - - - - - - -
10 - (2 + 3) * 4
- - - - - - - - - - - - - -
100 - 50 / 5
- - - - - - - - - - - - - -
((2 + 3) * (4 + 1))
- - - - - - - - - - - - - -
7 * 8 + 2 - 10
- - - - - - - - - - - - - -
20 / 4 / 5
- - - - - - - - - - - - - -
2 + 3 * 4 - 6 / 2
- - - - - - - - - - - - - -
(1 + 2) * (3 + 4) * (5 + 6)
- - - - - - - - - - - - - -
1000 + 2000 * 3
- - - - - - - - - - - - - -
50 - (10 - 5) - 3
- - - - - - - - - - - - - -
9 * 9 + 9 - 9 / 9
- - - - - - - - - - - - - -
(100 / 10) + (200 / 20)
- - - - - - - - - - - - - -
7 + 7 * 7 - 7
- - - - - - - - - - - - - -
18 / 3 + 4 * 2 - 1
- - - - - - - - - - - - - -
((10 - 5) * (20 / 4)) + 7
- - - - - - - - - - - - - -
144 / 12 / 3 + 8 * 2
- - - - - - - - - - - - - -
500 - (100 + 200) / 5
- - - - - - - - - - - - - -
(9 + 11) * (7 - 4) - (6 / 2)
- - - - - - - - - - - - - -
10000 / 100 + 50 * 4 - 30
```

**Rules:**

| Rule | Example |
|------|---------|
| One expression per line | `3 + 5 * 2` |
| Separators use only dashes and spaces | `- - - - -` |
| Whitespace is optional | `3+5*2` works too |
| Multi-digit numbers supported | `100`, `2000`, `10000` |
| Parentheses allowed and nestable | `((2 + 3) * (4 + 1))` |
| Blank lines preserved | Empty input line → empty output line |

**What is *not* supported in input:**

- Unary minus (`-5` as a standalone operand)
- Decimal numbers (`3.5`, `2.71`)
- Variables (`x`, `y`, `a1`)
- Functions (`sin`, `cos`, `sqrt`)
- Non-ASCII characters (`$`, `@`, letters, etc.)

If an invalid character appears in a line, the program writes `ERROR: Unexpected character: '...' at position N` for that line in `output.txt` and continues with the rest. One bad line does **not** crash the program.

---

## Output Format

**What this section explains:** How `data/output.txt` mirrors the input structure, replacing each expression with its computed result.

The output file has **exactly the same structure** as the input, but each expression is replaced by its computed **integer result**. Separators and blank lines are preserved unchanged.

**Sample `output.txt` (for the 20 expressions above):**

```
13
- - - - - - - - - - - - - -
16
- - - - - - - - - - - - - -
-10
- - - - - - - - - - - - - -
90
- - - - - - - - - - - - - -
25
- - - - - - - - - - - - - -
48
- - - - - - - - - - - - - -
1
- - - - - - - - - - - - - -
11
- - - - - - - - - - - - - -
231
- - - - - - - - - - - - - -
7000
- - - - - - - - - - - - - -
42
- - - - - - - - - - - - - -
89
- - - - - - - - - - - - - -
20
- - - - - - - - - - - - - -
49
- - - - - - - - - - - - - -
13
- - - - - - - - - - - - - -
32
- - - - - - - - - - - - - -
20
- - - - - - - - - - - - - -
440
- - - - - - - - - - - - - -
57
- - - - - - - - - - - - - -
270
```

**Mapping rules:**

| Input line type | Output line |
|-----------------|-------------|
| Expression (e.g. `3 + 5 * 2`) | Computed integer (`13`) |
| Separator (`- - - -`) | Unchanged |
| Blank line | Unchanged |
| Invalid expression | `ERROR: <message>` |

**Error handling:** If an expression cannot be evaluated, the output line begins with `ERROR:` followed by a description:

```
ERROR: Division by zero
ERROR: Mismatched parentheses: missing ')'
ERROR: Unexpected character: '$' at position 4
ERROR: Empty expression
```

This means one bad line does **not** break the whole program — every other expression is still evaluated and written correctly.

---

## Supported Operators

**What this section explains:** Which operators the evaluator understands, how they bind, and how integer division works.

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | Addition | `3 + 5` | `8` |
| `-` | Subtraction | `10 - 4` | `6` |
| `*` | Multiplication | `6 * 7` | `42` |
| `/` | Integer division | `8 / 4` | `2` |
| `( )` | Parentheses | `(2+3)*4` | `20` |

**Precedence** — higher number binds tighter:

| Level | Operators |
|-------|-----------|
| 2 (higher) | `*`, `/` |
| 1 (lower) | `+`, `-` |

**Example:** `3 + 5 * 2` = `3 + (5 * 2)` = `13`

**Associativity** — operators of equal precedence are evaluated left to right:

**Example:** `10 - 3 - 2` = `(10 - 3) - 2` = `5`, not `10 - (3 - 2)` = `9`.

**Example:** `20 / 4 / 5` = `(20 / 4) / 5` = `5 / 5` = `1`, not `20 / (4 / 5)`.

**Parentheses** — override both precedence and associativity. Anything inside is evaluated first.

**Example:** `(3 + 5) * 2` = `8 * 2` = `16`

**Example:** `((10 - 5) * (20 / 4)) + 7` = `(5 * 5) + 7` = `32`

**Integer division** — the `/` operator discards any fractional part of the result.

| Expression | Result | Note |
|------------|--------|------|
| `8 / 4` | `2` | Exact |
| `7 / 2` | `3` | Not 3.5 — remainder discarded |
| `9 / 3` | `3` | Exact |
| `144 / 12 / 3` | `4` | Evaluated left to right: (144/12)=12, then (12/3)=4 |

**Division by zero** — writes `ERROR: Division by zero` to that line in `output.txt`, and continues with the next expression.

---

## How It Works

**What this section explains:** The three-stage algorithm (tokenize, shunting-yard, postfix evaluation) and how the stack is used at each stage.

The program is a pipeline with three distinct stages. The **stack** data structure is central to stages 2 and 3.

```
[ Input string: "10 - (2 + 3) * 4" ]
                │
                ▼
        ┌───────────────────┐
        │  1. TOKENIZE      │   scan chars, group digits
        └───────────────────┘
                │
                ▼
   [ '10', '-', '(', '2', '+', '3', ')', '*', '4' ]
                │
                ▼
        ┌───────────────────┐
        │  2. INFIX→POSTFIX │   shunting-yard (Stack of operators)
        └───────────────────┘
                │
                ▼
   [ '10', '2', '3', '+', '4', '*', '-' ]
                │
                ▼
        ┌───────────────────┐
        │  3. EVAL POSTFIX  │   Stack of operands
        └───────────────────┘
                │
                ▼
              [ -10 ]
```

**Stage 1 — Tokenization**

The raw input string is scanned **character by character**. Each character is classified:

- **Digit** → start reading a number. Keep reading consecutive digits into one token. This is why `10` becomes `'10'` and not `'1'`, `'0'`.
- **Whitespace** → skip it.
- **Operator or parenthesis** (`+`, `-`, `*`, `/`, `(`, `)`) → becomes a single-character token.
- **Anything else** → raise `ValueError`.

```
"10 - (2 + 3) * 4"
→ ['10', '-', '(', '2', '+', '3', ')', '*', '4']
```

**Why not just split on spaces?** Because valid expressions may have no spaces at all: `10-(2+3)*4`. Character scanning handles both cases.

**Stage 2 — Infix → Postfix (Shunting-Yard)**

Infix notation has ambiguity about order of operations. Postfix (Reverse Polish Notation, or RPN) has none — operators come after their operands. Dijkstra's **shunting-yard algorithm** converts infix to postfix using a **stack of operators**:

| Token type | Action |
|------------|--------|
| Number | Send straight to output |
| Operator | Pop operators of higher-or-equal precedence from the stack to output, then push this one |
| `(` | Push onto stack |
| `)` | Pop from stack to output until matching `(` is found; discard the `(` |

```
['10', '-', '(', '2', '+', '3', ')', '*', '4']
→ ['10', '2', '3', '+', '4', '*', '-']
```

**Why postfix?** Because evaluation is then a simple left-to-right scan — no precedence rules to remember, no parentheses to match. All the intelligence happened during conversion.

**Stage 3 — Postfix Evaluation**

Now the postfix list is evaluated with a **stack of operands**:

| Token type | Action |
|------------|--------|
| Number | Push it onto the stack |
| Operator | Pop two operands, apply the operator, push the result |

**Full walkthrough of `['10', '2', '3', '+', '4', '*', '-']`:**

| Step | Token | Stack | Action |
|------|-------|-------|--------|
| 1 | `10` | `[10]` | push 10 |
| 2 | `2` | `[10, 2]` | push 2 |
| 3 | `3` | `[10, 2, 3]` | push 3 |
| 4 | `+` | `[10, 5]` | pop 3, 2 → push 5 |
| 5 | `4` | `[10, 5, 4]` | push 4 |
| 6 | `*` | `[10, 20]` | pop 4, 5 → push 20 |
| 7 | `-` | `[-10]` | pop 20, 10 → push -10 |

**Final answer:** `-10`

**Why a stack?**

- **Delays operations** until their operands are ready
- **Handles parentheses naturally** — pop to matching `(` on `)`
- **Makes postfix evaluation a clean push/pop loop** — no complex state

This is exactly why the stack is one of the fundamental data structures in computer science — it appears wherever we need to handle nested or delayed processing.

---

## Project Structure

**What this section explains:** Every file in the project and its specific role.

```
math-expression-evaluator/
│
├── src/
│   └── main.py                # Entire program logic
│                                #   - Stack class
│                                #   - tokenize()
│                                #   - infix_to_postfix()
│                                #   - eval_postfix()
│                                #   - evaluate()
│                                #   - process_file()
│                                #   - main()
│
├── tests/
│   └── test_stack.py          # 31 test methods (unittest)
│
├── data/
│   ├── input.txt              # 20 sample expressions
│   └── output.txt             # Generated results
│
├── docs/
│   └── report.md              # Full report (hard-copy submission)
│
├── README.md                  # This file
└── .gitignore                 # Git exclusions
```

| File | Purpose |
|------|---------|
| `src/main.py` | All program logic — Stack, tokenizer, shunting-yard, evaluator, file I/O |
| `tests/test_stack.py` | Unit tests for every component |
| `data/input.txt` | Sample expressions used to test the program (20 total) |
| `data/output.txt` | Produced when you run `py src/main.py` |
| `docs/report.md` | Full written report with introduction, design, testing, references |
| `.gitignore` | Excludes `__pycache__/`, `.venv/`, and IDE folders from Git |

**Why separate `src/` from `tests/`?** So the program and its tests are logically distinct. Tests import from `src/` by adding it to `sys.path` at the top of `test_stack.py`.

**Why a `data/` folder?** Input and output are data, not code. Keeping them separate makes the program reusable — you can swap in a different `input.txt` and rerun.

**Why a `docs/` folder?** The full written report (for the hard-copy submission) lives separately from the code documentation (this README).

---

## Assumptions & Limitations

**What this section explains:** What the program assumes about input, what it does not support, and how it handles errors.

**Assumptions:**

1. Arithmetic is **integer-only** — no floats are used or produced
2. Operators are **binary** — each takes exactly two operands
3. Parentheses are **balanced** — every `(` has a matching `)`
4. Only **literal integers** appear — no variables, functions, or constants
5. **Whitespace is optional** — expressions may or may not have spaces

**Limitations — the program does not support:**

| Feature | Reason |
|---------|--------|
| Floating point (`3.5`) | Integer-only arithmetic per assignment |
| Unary minus (`-5` standalone) | Only binary subtraction implemented |
| Exponentiation (`^`, `**`) | Not in scope |
| Modulo (`%`) | Not in scope |
| Variables (`x`) | Not in scope |
| Functions (`sin`, `cos`) | Not in scope |
| Decimal points | Integer-only |
| Scientific notation (`1e3`) | Integer-only |
| Comments in `input.txt` | Not required by assignment |

**Error recovery:** Each expression is evaluated independently. If one line fails (e.g., division by zero, mismatched parentheses, invalid character), the program writes an `ERROR:` line for that expression and continues with the next. This means a single bad line does **not** abort the entire file processing.

---

## Troubleshooting

**What this section explains:** Common problems and how to fix them.

**Problem:** `py: command not found` or `python: command not found`

**Fix:** Python is not on your PATH. Either:
- Reinstall Python and check **"Add python.exe to PATH"** during installation
- Use `python3` instead of `python` on macOS/Linux
- On Windows, try `py` (the Python launcher)

**Problem:** `ModuleNotFoundError: No module named 'main'` when running tests

**Fix:** Run the tests from the **project root** (not from inside `tests/`):
```bash
cd math-expression-evaluator
py -m unittest discover tests -v
```

**Problem:** `FileNotFoundError: Input file not found: .../data/input.txt`

**Fix:** Make sure `data/input.txt` exists. If you cloned the repo, it should already be there. If you deleted it, recreate it with some expressions.

**Problem:** `PermissionError: [Errno 13] Permission denied: '.../data/output.txt'`

**Fix:** The output file may be open in an editor (PyCharm, VS Code) that has locked it. Close the file in the editor and try again. Alternatively, the program writes to a temporary file first and uses `os.replace()` to swap it in — this usually avoids the issue.

**Problem:** `SyntaxError: invalid syntax` on a line like `print "hello"`

**Fix:** You're using Python 2 syntax in Python 3. This project requires Python 3.8+. Check with `py --version`.

**Problem:** Output file is empty

**Fix:** Check that `data/input.txt` has content. If it's empty, `output.txt` will be empty too.

---

## FAQ

**What section is this?** Frequently asked questions about the project.

**Q: Why is `(8 / 4) + 7 * 2` shown as `17` in the assignment but `16` in the output?**

Because the correct answer under standard operator precedence is 16 (`2 + 14`). The "17" in the assignment brief appears to be a typo. See the "Note on the Assignment Example" section below for a full discussion.

**Q: Can I use Python's `eval()` instead?**

No. The assignment requires demonstrating a stack-based approach. Using `eval()` would defeat the entire purpose and would likely lose marks on the "Stack Operations" criterion (15 marks).

**Q: Can I add more expressions to `input.txt`?**

Yes. The file currently has 20 expressions but you can add as many as you want. Each expression on its own line, separated by dash-only lines.

**Q: What if a line has an error?**

The program writes an `ERROR: <message>` line for that expression and continues with the next. It does not crash.

**Q: Can I use floating-point numbers?**

No, the program uses integer arithmetic only (`//` division). This matches the assignment specification.

**Q: How do I add my own expressions?**

Edit `data/input.txt` — one expression per line, separated by lines containing only dashes and spaces. Then run `py src/main.py`.

**Q: What does `//` mean in the code?**

`//` is Python's integer division operator. `7 // 2` is `3` (the remainder is discarded).

**Q: How do I check that my input file has the right format?**

The program classifies each line:
- Blank lines → preserved
- Lines with only dashes and spaces → treated as separators
- Everything else → treated as an expression

If a line contains characters that are not digits, whitespace, or `+-*/()`, it produces an `ERROR:` line.

**Q: Can I run this on macOS or Linux?**

Yes. Use `python3` instead of `py`:
```bash
python3 src/main.py
python3 -m unittest discover tests -v
```

**Q: How do I know the program is done?**

It prints `Done.` to the terminal and exits with code 0.

---

## Note on the Assignment Example

**What this section explains:** Why our program outputs 16 for `(8 / 4) + 7 * 2` while the assignment brief shows 17.

The assignment brief shows:

```
(8 / 4) + 7 * 2  →  17
```

Under **standard operator precedence**, the correct value is:

```
(8 / 4) + (7 * 2)
= 2 + 14
= 16
```

**Our program outputs 16** — the mathematically correct answer.

Let's verify no reasonable interpretation could produce 17:

| Interpretation | Working | Result |
|----------------|---------|--------|
| Standard precedence: `(8/4) + (7*2)` | 2 + 14 | **16** ✅ |
| Left-to-right: `((8/4) + 7) * 2` | (2 + 7) * 2 = 18 | 18 ❌ |
| Right-to-left: `8 / ((4+7) * 2)` | 8 / 22 | Non-integer ❌ |
| `8 / (4 + 7) * 2` | 0.72 * 2 | Non-integer ❌ |

**No standard rule produces 17.** We conclude the "17" in the brief is a **typo**. Our program outputs the mathematically correct value (16) and this discrepancy is documented transparently rather than hidden.

If the lecturer confirms 17 was intended (unlikely), the correct response is to clarify the rule being used — not to silently change the math.

---

## Author

**What this section explains:** Submission metadata for this assignment.

**Joshua Mohamed Katibi Yaffa**  
Student ID: **905004075**   
Module: **DCOMP320 — Data Structures and Algorithms**   
Class :  **BSEM2101**  
Semester: **5**, Year: **3**  
Institution: **Limkokwing University of Creative Technology — Sierra Leone**  
Submission Date: **09 / 10 / 2026**

**Assignment Brief:**

> DATA STRUCTURES AND ALGORITHM ANALYSIS (DCOMP320)  
> BSEM2101 — Semester 5 — Assignment

**Related document:**

- `docs/report.md` — full written report with introduction, data structure discussion, program design, testing analysis, and references.

---

## License

This project was created for the DCOMP320 assignment at Limkokwing University. It may be freely used for educational purposes.

---

*End of README.*