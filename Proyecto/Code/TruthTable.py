import itertools
import re

def translate_keywords(expr, variable_names):
    # Convertir a minúsculas para procesamiento uniforme
    result = expr.lower()
    
    # Manejar "no" en todas sus formas ANTES de otros operadores
    # no(expresión) -> (not expresión)
    result = re.sub(r'\bno\s*\(([^)]+)\)', r'(not (\1))', result)
    # " no " -> " not "
    result = re.sub(r'\s+no\s+', r' not ', result)
    
    # Operadores complejos con paréntesis
    # Condicional: (A condicional B) -> ((not A) or B)
    result = re.sub(r'\(\s*([^)]+)\s+condicional\s+([^)]+)\s*\)', r'((not (\1)) or (\2))', result)
    # Bicondicional: (A bicondicional B) -> (A == B)  
    result = re.sub(r'\(\s*([^)]+)\s+bicondicional\s+([^)]+)\s*\)', r'((\1) == (\2))', result)
    # XOR: (A xor B) -> (A != B)
    result = re.sub(r'\(\s*([^)]+)\s+xor\s+([^)]+)\s*\)', r'((\1) != (\2))', result)
    
    # Operadores básicos (con espacios obligatorios para evitar conflictos)
    result = re.sub(r'\s+y\s+', r' and ', result)
    result = re.sub(r'\s+o\s+', r' or ', result)
    
    # Restaurar variables originales (solo palabras completas)
    for name in variable_names:
        # Usar límites de palabra para evitar reemplazar partes de 'or', 'and', etc.
        pattern = r'\b' + re.escape(name.lower()) + r'\b'
        result = re.sub(pattern, name, result)
    
    return result

class TruthTable:
    def __init__(self, symbols, names, expression):
        self.symbols = symbols
        self.names = names
        self.expression = expression

    def generate(self):
        expr_eval = translate_keywords(self.expression, self.names)
        
        header = "  ".join(name.center(8) for name in self.names) + "  |  " + self.expression
        print("\n" + header)
        print("-" * len(header))

        for values in itertools.product([True, False], repeat=len(self.names)):
            context = dict(zip(self.names, values))
            
            try:
                result = eval(expr_eval, {}, context)
            except Exception as e:
                print(f"Error en la expresion: {e}")
                print(f"Expresión que causó el error: {expr_eval}")
                print(f"Contexto: {context}")
                return
                
            row = "  ".join(str(context[name]).center(8) for name in self.names)
            print(f"{row}  |  {result}")