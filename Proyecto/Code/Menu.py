from TruthTable import TruthTable
from MenuOptions import MenuOptions

class Menu:
    def __init__(self):
        self.menu_options = MenuOptions()
    
    def get_names(self):
        print("Ingrese hasta cinco proposiciones.")
        entrada = input("Proposiciones (separados por comas): ")
        names = [n.strip() for n in entrada.split(",") if n.strip()]
        if not 1 <= len(names) <= 5:
            print("Cantidad inválida. Debe ingresar entre 1 y 5 nombres.")
            return None
        return names

    def get_expression(self, symbols):
        self.menu_options.show_help()
        return input("Expresion: ")
    
    def generate_truth_table(self):
        """Ejecuta el proceso de generación de tabla de verdad"""
        names = self.get_names()
        if names is None:
            return
        symbols = ['p', 'q', 'r', 's', 't'][:len(names)]
        expr = self.get_expression(symbols)
        table = TruthTable(symbols, names, expr)
        table.generate()

    def run(self):
        """Ejecuta el bucle principal del menú"""
        while True:
            self.menu_options.display_menu()
            choice = self.menu_options.get_user_choice()
            
            if choice == 1:
                self.generate_truth_table()
                input("\nPresione Enter para continuar...")
            elif choice == 2:
                print("Saliendo del programa...")
                break