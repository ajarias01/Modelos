import itertools
import re

def translate_keywords(expr):
    expr = expr.lower()

    # Operadores básicos
    expr = expr.replace(" y ", " and ")
    expr = expr.replace(" o ", " or ")
    expr = expr.replace(" no ", " not ")
    expr = re.sub(r'\bno\((\w+)\)', r'(not \1)', expr)

    # Condicional: (A) condicional (B)  =>  ((not A) or B)
    expr = re.sub(r'\(\s*(.+?)\s*\)\s*condicional\s*\(\s*(.+?)\s*\)', r'((not (\1)) or (\2))', expr)

    # Bicondicional: (A) bicondicional (B)  =>  (A == B)
    expr = re.sub(r'\(\s*(.+?)\s*\)\s*bicondicional\s*\(\s*(.+?)\s*\)', r'((\1) == (\2))', expr)

    # XOR: (A) xor (B) => (A != B)
    expr = re.sub(r'\(\s*(.+?)\s*\)\s*xor\s*\(\s*(.+?)\s*\)', r'((\1) != (\2))', expr)

    return expr

class TruthTable:
    def __init__(self, symbols, names, expression):
        self.symbols = symbols
        self.names = names
        self.expression = expression

    def generate(self):
        expr_eval = translate_keywords(self.expression)
        header = "  ".join(name.center(8) for name in self.names) + "  |  " + self.expression
        print("\n" + header)
        print("-" * len(header))

        for values in itertools.product([True, False], repeat=len(self.names)):
            context = dict(zip(self.names, values))
            eval_context = {sym: context[name] for sym, name in zip(self.symbols, self.names)}
            try:
                result = eval(expr_eval, {}, eval_context)
            except Exception as e:
                print("Error en la expresion:", e)
                return
            row = "  ".join(str(context[name]).center(8) for name in self.names)
            print(f"{row}  |  {result}")
