from TruthTable import TruthTable

class Menu:
    def get_names(self):
        print("Ingrese hasta cinco proposiciones.")
        entrada = input("Proposiciones (separados por comas): ")
        names = [n.strip() for n in entrada.split(",") if n.strip()]
        if not 1 <= len(names) <= 5:
            print("Cantidad inválida. Debe ingresar entre 1 y 5 nombres.")
            return None
        return names

    def get_expression(self, symbols):
        print("\nUse los siguientes simbolos:")
        print("  y, o, no, (p condicional q), (p bicondicional q), (p xor q)")
        print("Ejemplo: (p condicional q) o no(r)")
        return input("Expresion: ")

    def run(self):
        names = self.get_names()
        if names is None:
            return
        symbols = ['p', 'q', 'r', 's', 't'][:len(names)]
        expr = self.get_expression(symbols)
        table = TruthTable(symbols, names, expr)
        table.generate()

if __name__ == "__main__":
    Menu().run()
