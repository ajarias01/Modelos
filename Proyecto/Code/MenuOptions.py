class MenuOptions:
    def __init__(self):
        self.options = {
            1: {
                'title': 'Generar tabla de verdad',
                'description': 'Crear una tabla de verdad para proposiciones lógicas'
            },
            2: {
                'title': 'Salir',
                'description': 'Salir del programa'
            }
        }
    
    def display_menu(self):
        print("\n" + "="*50)
        print("GENERADOR DE TABLAS DE VERDAD".center(50))
        print("="*50)
        for key, option in self.options.items():
            print(f"{key}. {option['title']}")
            print(f"   {option['description']}\n")
    
    def get_user_choice(self):
        while True:
            try:
                choice = int(input("Seleccione una opción: "))
                if choice in self.options:
                    return choice
                else:
                    print(f"Opción inválida. Seleccione entre 1 y {len(self.options)}.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
    
    def show_help(self):
        print("\nUse los siguientes operadores lógicos en español:")
        print("  y, o, no, condicional, bicondicional, xor")
        print("Ejemplo:")
        print("  (primera proposicion condicional segunda proposicion) o no(tercera proposicion)\n")
