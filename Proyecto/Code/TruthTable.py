import itertools
import re

def normalize_name(name):
    """Convierte nombres con espacios a nombres válidos para Python, ejemplo 'juan juega' -> 'juan_juega'"""
    return re.sub(r'\s+', '_', name.strip())

def translate_keywords(expr, variable_names):
    # Convierte todo a minúsculas para el procesamiento uniforme
    result = expr.lower()

    # Reemplazar nombres originales (con espacios) por normalizados (sin espacios)
    for name in variable_names:
        normalized = normalize_name(name)
        pattern = r'\b' + re.escape(name.lower()) + r'\b'
        result = re.sub(pattern, normalized, result)

    # Manejar "no" antes de otros operadores
    result = re.sub(r'\bno\s*\(([^)]+)\)', r'(not (\1))', result)
    result = re.sub(r'\s+no\s+', r' not ', result)

    # Operadores compuestos
    result = re.sub(r'\(\s*([^)]+)\s+condicional\s+([^)]+)\s*\)', r'((not (\1)) or (\2))', result)
    result = re.sub(r'\(\s*([^)]+)\s+bicondicional\s+([^)]+)\s*\)', r'((\1) == (\2))', result)
    result = re.sub(r'\(\s*([^)]+)\s+xor\s+([^)]+)\s*\)', r'((\1) != (\2))', result)

    # Operadores básicos
    result = re.sub(r'\s+y\s+', r' and ', result)
    result = re.sub(r'\s+o\s+', r' or ', result)

    return result

class TruthTable:
    def __init__(self, symbols, names, expression):
        self.original_names = names                # Nombres originales con espacios
        self.normalized_names = [normalize_name(n) for n in names]  # Nombres sin espacios
        self.expression = expression

    def generate(self):
        expr_eval = translate_keywords(self.expression, self.original_names)

        header = "  ".join(name.center(15) for name in self.original_names) + "  |  " + self.expression
        print("\n" + header)
        print("-" * len(header))

        for values in itertools.product([True, False], repeat=len(self.original_names)):
            context = dict(zip(self.normalized_names, values))
            try:
                result = eval(expr_eval, {}, context)
            except Exception as e:
                print(f"Error en la expresión: {e}")
                print(f"Expresión que causó el error: {expr_eval}")
                print(f"Contexto: {context}")
                return
            
            row = "  ".join(str(val).center(15) for val in values)
            print(f"{row}  |  {result}")
