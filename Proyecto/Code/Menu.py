import itertools
import re

def normalize_name(name):
    return re.sub(r'\s+', '_', name.strip())

def translate_keywords(expr, variable_names):
    result = expr.lower()
    
    # Manejar "no"
    result = re.sub(r'\bno\s*\(([^)]+)\)', r'(not (\1))', result)
    result = re.sub(r'\s+no\s+', r' not ', result)
    
    # Operadores complejos
    result = re.sub(r'\(\s*([^)]+)\s+condicional\s+([^)]+)\s*\)', r'((not (\1)) or (\2))', result)
    result = re.sub(r'\(\s*([^)]+)\s+bicondicional\s+([^)]+)\s*\)', r'((\1) == (\2))', result)
    result = re.sub(r'\(\s*([^)]+)\s+xor\s+([^)]+)\s*\)', r'((\1) != (\2))', result)
    
    # Operadores básicos
    result = re.sub(r'\s+y\s+', r' and ', result)
    result = re.sub(r'\s+o\s+', r' or ', result)
    
    # Reemplazar variables originales por normalizadas
    for name in variable_names:
        normalized = normalize_name(name)
        pattern = r'\b' + re.escape(name.lower()) + r'\b'
        result = re.sub(pattern, normalized, result)
    
    return result

class TruthTable:
    def __init__(self, symbols, names, expression):
        self.original_names = names
        self.normalized_names = [normalize_name(n) for n in names]
        self.expression = expression

def generate(self):
    expr_eval = translate_keywords(self.expression, self.original_names)
    
    header = "  ".join(name.center(20) for name in self.original_names) + "  |  Resultado"
    print("\n" + header)
    print("-" * len(header))
    
    for values in itertools.product([True, False], repeat=len(self.original_names)):
        context = dict(zip(self.normalized_names, values))
        try:
            result = eval(expr_eval, {}, context)  # Usar expr_eval ya traducida
        except Exception as e:
            print(f"\nError en la expresión: {e}")
            print(f"Expresión traducida: {expr_eval}")
            print(f"Contexto: {context}")
            return
        
        row = "  ".join(str(val).center(20) for val in values)
        print(f"{row}  |  {result}")
