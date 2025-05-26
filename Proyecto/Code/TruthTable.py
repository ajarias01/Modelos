import itertools
import re

def normalize_name(name):
    # Normaliza nombres reemplazando espacios por guion bajo
    return re.sub(r'\s+', '_', name.strip())

def replace_vars(expr, names):
    # Reemplaza nombres originales en la expresión por su versión normalizada (sin espacios)
    for name in names:
        expr = re.sub(r'\b' + re.escape(name.lower()) + r'\b', normalize_name(name), expr)
    return expr

def parse_expr(expr, context):
    expr = expr.strip()

    # Evaluar paréntesis más internos primero
    while '(' in expr:
        start = expr.rfind('(')
        end = expr.find(')', start)
        if end == -1:
            raise Exception("Paréntesis no balanceados")
        inner = expr[start+1:end]
        val = parse_expr(inner, context)
        expr = expr[:start] + str(val) + expr[end+1:]

    # Evaluar NOT (no)
    if expr.startswith('no '):
        return not parse_expr(expr[3:], context)

    # Operadores lógicos en orden

    # Condicional
    if ' condicional ' in expr:
        a, b = expr.split(' condicional ', 1)
        return (not parse_expr(a, context)) or parse_expr(b, context)

    # Bicondicional
    if ' bicondicional ' in expr:
        a, b = expr.split(' bicondicional ', 1)
        return parse_expr(a, context) == parse_expr(b, context)

    # XOR
    if ' xor ' in expr:
        a, b = expr.split(' xor ', 1)
        return parse_expr(a, context) != parse_expr(b, context)

    # OR (o)
    if ' o ' in expr:
        parts = expr.split(' o ')
        return any(parse_expr(p, context) for p in parts)

    # AND (y)
    if ' y ' in expr:
        parts = expr.split(' y ')
        return all(parse_expr(p, context) for p in parts)

    # Si es variable normalizada
    if expr in context:
        return context[expr]

    # Valores booleanos literales
    if expr == 'True':
        return True
    if expr == 'False':
        return False

    raise Exception(f"Expresión inválida o variable desconocida: '{expr}'")

class TruthTable:
    def __init__(self, names, expression):
        self.names = names
        self.norm_names = [normalize_name(n) for n in names]
        self.expression = replace_vars(expression.lower(), names)

    def generate(self):
        header = "  ".join(name.center(20) for name in self.names) + "  |  " + self.expression
        print("\n" + header)
        print("-" * len(header))

        for values in itertools.product([True, False], repeat=len(self.names)):
            context = dict(zip(self.norm_names, values))
            try:
                result = parse_expr(self.expression, context)
            except Exception as e:
                print(f"Error evaluando expresión: {e}")
                return

            row = "  ".join(str(val).center(20) for val in values)
            print(f"{row}  |  {result}")
