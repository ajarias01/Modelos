from TruthTable import TruthTable
from MenuOptions import MenuOptions

class Menu:
    def __init__(self):
        self.menu_options = MenuOptions()
    
    def get_names(self):
        print("Ingrese hasta cinco proposiciones (pueden tener espacios).")
        entrada = input("Proposiciones (separados por comas): ")
        names = [n.strip() for n in entrada.split(",") if n.strip()]
        if not 1 <= len(names) <= 5:
            print("Cantidad inválida. Debe ingresar entre 1 y 5 nombres.")
            return None
        return names

    def get_expression(self):
        self.menu_options.show_help()
        return input("Expresión lógica: ")
    
    def generate_truth_table(self):
        names = self.get_names()
        if names is None:
            return
        expr = self.get_expression()
        table = TruthTable(names, expr)
        table.generate()

    def run(self):
        while True:
            self.menu_options.display_menu()
            choice = self.menu_options.get_user_choice()
            
            if choice == 1:
                self.generate_truth_table()
                input("\nPresione Enter para continuar...")
            elif choice == 2:
                print("Saliendo del programa...")
                break
