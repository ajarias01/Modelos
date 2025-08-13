from tkinter import *
from tkinter import messagebox
import threading
import time
from game_logic import WordCraftGame
from Utils.data_structures import GameState

class WordCraftGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("WordCraft")
        self.root.resizable(False, False)
        self.root.geometry("800x600")
        self.root.iconbitmap("Images/iconoVentana.ico")
        self.root.config(bg="black")
        
        # Inicializar el juego
        self.game = WordCraftGame()
        
        # Variables de la interfaz
        self.current_menu_index = 0
        self.current_letter_index = 0
        self.current_position = 0
        self.word_positions = []
        self.max_word_length = 4  # Máximo 4 letras por palabra
        
        # Widgets principales
        self.main_frame = None
        self.game_frame = None
        self.menu_labels = []
        self.letter_labels = []
        self.word_display_labels = []
        self.info_labels = {}
        
        # Variables del temporizador visual
        self.timer_label = None
        self.timer_running = False
        
        self.create_main_menu()
        self.bind_events()
        
    def create_main_menu(self):
        """Crea el menú principal"""
        self.clear_screen()
        
        self.main_frame = Frame(self.root, bg="black")
        self.main_frame.pack(fill=BOTH, expand=True)
        
        # Texto de bienvenida
        welcome_text = """¡Bienvenido a WordCraft!
Forma palabras usando las letras disponibles.
Este juego te ayudará a mejorar tu vocabulario
mientras te diviertes.

Usa las flechas ↑↓ para navegar y Enter para seleccionar."""
        
        welcome_label = Label(self.main_frame, text=welcome_text,
                             font=("Arial", 12),
                             fg="white", bg="black",
                             justify=LEFT)
        welcome_label.pack(pady=20, padx=20)
        
        # Opciones del menú
        self.menu_options = ["Jugar", "Instrucciones", "Salir"]
        self.current_menu_index = 0
        self.menu_labels = []
        
        for i, option in enumerate(self.menu_options):
            label = Label(self.main_frame, text=option,
                         font=("Arial", 14), bg="black", fg="white")
            label.pack(pady=5)
            self.menu_labels.append(label)
        
        self.update_menu_display()
    
    def create_player_selection(self):
        """Crea la pantalla de selección de jugadores"""
        self.clear_screen()
        
        self.main_frame = Frame(self.root, bg="black")
        self.main_frame.pack(fill=BOTH, expand=True)
        
        title_label = Label(self.main_frame, text="Selecciona el número de jugadores",
                           font=("Arial", 16, "bold"), fg="white", bg="black")
        title_label.pack(pady=30)
        
        self.menu_options = ["1 Jugador", "2 Jugadores", "Volver"]
        self.current_menu_index = 0
        self.menu_labels = []
        
        for i, option in enumerate(self.menu_options):
            label = Label(self.main_frame, text=option,
                         font=("Arial", 14), bg="black", fg="white")
            label.pack(pady=10)
            self.menu_labels.append(label)
        
        self.update_menu_display()
    
    def create_instructions(self):
        """Crea la pantalla de instrucciones"""
        self.clear_screen()
        
        self.main_frame = Frame(self.root, bg="black")
        self.main_frame.pack(fill=BOTH, expand=True)
        
        instructions_text = """INSTRUCCIONES DEL JUEGO

OBJETIVO:
Forma la mayor cantidad de palabras válidas usando las letras disponibles.

CONTROLES:
• Flechas ←→: Seleccionar letra
• Flechas ↑↓: Cambiar posición en la palabra
• Enter: Colocar letra seleccionada
• Espacio: Enviar palabra completa
• Backspace: Eliminar letra actual
• Escape: Volver al menú

REGLAS:
• Las palabras deben tener exactamente 4 letras
• Cada letra solo se puede usar una vez
• Las palabras deben estar en el diccionario
• Tienes 5 minutos por turno

PUNTUACIÓN:
• Letras comunes (A,E,I,O,U,L,N,R,S,T): 1 punto
• Letras menos comunes (C,D,G,M,B,P): 2-3 puntos  
• Letras raras (J,K,Q,W,X,Z): 5-10 puntos
• Bonus por longitud: +5 puntos (4+ letras), +10 puntos (6+ letras)

Presiona Enter para volver al menú principal."""
        
        instructions_label = Label(self.main_frame, text=instructions_text,
                                  font=("Arial", 10), fg="white", bg="black",
                                  justify=LEFT)
        instructions_label.pack(pady=20, padx=20)
    
    def create_game_screen(self):
        """Crea la pantalla principal del juego"""
        self.clear_screen()
        
        self.game_frame = Frame(self.root, bg="black")
        self.game_frame.pack(fill=BOTH, expand=True)
        
        # Información del jugador y puntaje
        info_frame = Frame(self.game_frame, bg="black")
        info_frame.pack(pady=10)
        
        if self.game.num_players == 2:
            player_info = f"Jugador {self.game.current_player}"
        else:
            player_info = "Jugador 1"
        
        self.info_labels['player'] = Label(info_frame, text=player_info,
                                          font=("Arial", 14, "bold"),
                                          fg="yellow", bg="black")
        self.info_labels['player'].pack()
        
        # Temporizador
        self.timer_label = Label(info_frame, text=f"Tiempo: {self.game.get_current_time_left()}s",
                                font=("Arial", 12), fg="red", bg="black")
        self.timer_label.pack()
        
        # Puntajes
        score_text = f"Puntuación: {self.game.player1_score}"
        if self.game.num_players == 2:
            score_text += f"  |  Jugador 2: {self.game.player2_score}"
        
        self.info_labels['score'] = Label(info_frame, text=score_text,
                                         font=("Arial", 12), fg="white", bg="black")
        self.info_labels['score'].pack()
        
        # Letras disponibles
        letters_frame = Frame(self.game_frame, bg="black")
        letters_frame.pack(pady=20)
        
        Label(letters_frame, text="Letras disponibles:",
              font=("Arial", 12), fg="white", bg="black").pack()
        
        available_letters = self.game.get_available_letters_display()
        letters_display_frame = Frame(letters_frame, bg="black")
        letters_display_frame.pack()
        
        self.letter_labels = []
        for i, letter in enumerate(available_letters):
            label = Label(letters_display_frame, text=letter,
                         font=("Arial", 14, "bold"), bg="gray", fg="white",
                         width=3, height=2, relief=RAISED)
            label.grid(row=0, column=i, padx=2, pady=2)
            self.letter_labels.append(label)
        
        self.current_letter_index = 0
        self.update_letter_selection()
        
        # Área de formación de palabras
        word_frame = Frame(self.game_frame, bg="black")
        word_frame.pack(pady=20)
        
        Label(word_frame, text="Palabra actual:",
              font=("Arial", 12), fg="white", bg="black").pack()
        
        word_display_frame = Frame(word_frame, bg="black")
        word_display_frame.pack()
        
        self.word_display_labels = []
        self.word_positions = [''] * self.max_word_length
        self.current_position = 0
        
        for i in range(self.max_word_length):
            label = Label(word_display_frame, text="_",
                         font=("Arial", 14, "bold"), bg="white", fg="black",
                         width=3, height=2, relief=SUNKEN)
            label.grid(row=0, column=i, padx=2, pady=2)
            self.word_display_labels.append(label)
        
        self.update_word_display()
        
        # Instrucciones de controles
        controls_text = "Controles: ←→ cambiar letra | ↑↓ cambiar posición | Enter colocar letra | Espacio enviar palabra | Backspace borrar | Escape menú"
        Label(self.game_frame, text=controls_text,
              font=("Arial", 9), fg="gray", bg="black").pack(pady=10)
        
        # Palabras formadas
        words_frame = Frame(self.game_frame, bg="black")
        words_frame.pack(pady=10)
        
        if self.game.player1_words:
            words_text = "Palabras: " + ", ".join(self.game.player1_words)
            Label(words_frame, text=words_text,
                  font=("Arial", 10), fg="green", bg="black").pack()
        
        # Iniciar temporizador
        self.start_visual_timer()
    
    def update_menu_display(self):
        """Actualiza la visualización del menú"""
        for i, label in enumerate(self.menu_labels):
            if i == self.current_menu_index:
                label.config(bg="white", fg="black", font=("Arial", 14, "bold"))
            else:
                label.config(bg="black", fg="white", font=("Arial", 14))
    
    def update_letter_selection(self):
        """Actualiza la selección de letras disponibles"""
        for i, label in enumerate(self.letter_labels):
            if i == self.current_letter_index:
                label.config(bg="yellow", fg="black")
            else:
                label.config(bg="gray", fg="white")
    
    def update_word_display(self):
        """Actualiza la visualización de la palabra en formación"""
        for i, label in enumerate(self.word_display_labels):
            if self.word_positions[i]:
                label.config(text=self.word_positions[i], bg="lightgreen", fg="black")
            else:
                label.config(text="_", bg="white", fg="black")
            
            # Resaltar posición actual
            if i == self.current_position:
                if self.word_positions[i]:
                    label.config(bg="orange")
                else:
                    label.config(bg="lightblue")
    
    def start_visual_timer(self):
        """Inicia el temporizador visual"""
        self.timer_running = True
        self.game.start_timer()
        
        def update_timer():
            if self.timer_running:
                if self.timer_label:
                    time_left = self.game.get_current_time_left()
                    self.timer_label.config(text=f"Tiempo: {time_left}s")
                    
                    if time_left <= 10:
                        self.timer_label.config(fg="red")
                    elif time_left <= 30:
                        self.timer_label.config(fg="orange")
                    else:
                        self.timer_label.config(fg="white")
                    
                    if time_left <= 0:
                        # Detener el temporizador y terminar el turno
                        self.timer_running = False
                        self.game.stop_timer()
                        # Usar after() para ejecutar end_turn en el hilo principal de Tkinter
                        self.root.after(0, self.end_turn)
                        return
                
                # Programar la siguiente actualización solo si el temporizador sigue corriendo
                if self.timer_running and self.game.get_current_time_left() > 0:
                    self.root.after(1000, update_timer)
        
        # Iniciar la primera actualización
        update_timer()
    
    def stop_visual_timer(self):
        """Detiene el temporizador visual"""
        self.timer_running = False
        self.game.stop_timer()
    
    def place_letter(self):
        """Coloca la letra seleccionada en la posición actual"""
        if self.current_letter_index < len(self.letter_labels):
            available_letters = self.game.get_available_letters_display()
            if self.current_letter_index < len(available_letters):
                letter = available_letters[self.current_letter_index]
                self.word_positions[self.current_position] = letter
                self.move_to_next_position()
                self.update_word_display()
    
    def move_to_next_position(self):
        """Mueve a la siguiente posición vacía"""
        for i in range(self.current_position + 1, self.max_word_length):
            if not self.word_positions[i]:
                self.current_position = i
                return
        # Si no hay posiciones vacías hacia adelante, quedarse en la actual
    
    def remove_current_letter(self):
        """Elimina la letra en la posición actual"""
        self.word_positions[self.current_position] = ''
        self.update_word_display()
    
    def submit_current_word(self):
        """Envía la palabra actual para validación"""
        word = ''.join([pos for pos in self.word_positions if pos]).strip()
        
        if not word:
            messagebox.showwarning("Palabra vacía", "Debes formar una palabra antes de enviarla.")
            return
        
        success, message = self.game.submit_word(word)
        
        if success:
            messagebox.showinfo("¡Palabra válida!", message)
            self.reset_word_formation()
            self.refresh_game_screen()
        else:
            messagebox.showerror("Palabra inválida", message)
    
    def reset_word_formation(self):
        """Reinicia la formación de palabras"""
        self.word_positions = [''] * self.max_word_length
        self.current_position = 0
    
    def refresh_game_screen(self):
        """Actualiza toda la pantalla del juego"""
        self.create_game_screen()
    
    def end_turn(self):
        """Termina el turno del jugador actual"""
        self.stop_visual_timer()
        
        # Llamar a end_turn del juego para manejar la lógica
        self.game.end_turn()
        
        # Verificar si hay una nueva ronda por empate
        if self.game.new_round_started:
            self.game.new_round_started = False  # Reset la flag
            messagebox.showinfo("¡Empate!", 
                               f"¡Empate con {self.game.player1_score} puntos cada uno!\n"
                               f"Nueva ronda con letras diferentes.")
            self.refresh_game_screen()
        elif self.game.state_machine.current_state == GameState.GAME_OVER:
            self.show_game_over()
        elif self.game.num_players == 2:
            # Si es un juego de 2 jugadores y no ha terminado, refrescar la pantalla
            self.refresh_game_screen()
        else:
            # Si es un juego de 1 jugador, terminar
            self.show_game_over()
    
    def show_game_over(self):
        """Muestra la pantalla de fin de juego"""
        self.stop_visual_timer()
        summary = self.game.get_game_summary()
        
        result_text = f"¡Juego terminado!\n\n"
        result_text += f"Jugador 1: {summary['player1_score']} puntos\n"
        result_text += f"Palabras: {', '.join(summary['player1_words']) if summary['player1_words'] else 'Ninguna'}\n\n"
        
        if self.game.num_players == 2:
            result_text += f"Jugador 2: {summary['player2_score']} puntos\n"
            result_text += f"Palabras: {', '.join(summary['player2_words']) if summary['player2_words'] else 'Ninguna'}\n\n"
            
            if summary['winner'] == 1:
                result_text += "¡Jugador 1 gana!"
            elif summary['winner'] == 2:
                result_text += "¡Jugador 2 gana!"
            else:
                result_text += "¡Empate!"
        
        messagebox.showinfo("Fin del juego", result_text)
        self.game.reset_game()
        self.create_main_menu()
    
    def clear_screen(self):
        """Limpia la pantalla actual"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def handle_key_event(self, event):
        """Maneja los eventos de teclado"""
        if self.game.state_machine.current_state == GameState.MENU:
            self.handle_menu_keys(event)
        elif self.game.state_machine.current_state == GameState.PLAYER_SELECTION:
            self.handle_player_selection_keys(event)
        elif self.game.state_machine.current_state == GameState.INSTRUCTIONS:
            self.handle_instructions_keys(event)
        elif self.game.state_machine.current_state in [GameState.PLAYER1_TURN, GameState.PLAYER2_TURN]:
            self.handle_game_keys(event)
    
    def handle_menu_keys(self, event):
        """Maneja las teclas en el menú principal"""
        if event.keysym == "Up":
            self.current_menu_index = (self.current_menu_index - 1) % len(self.menu_options)
            self.update_menu_display()
        elif event.keysym == "Down":
            self.current_menu_index = (self.current_menu_index + 1) % len(self.menu_options)
            self.update_menu_display()
        elif event.keysym == "Return":
            self.select_menu_option()
    
    def handle_player_selection_keys(self, event):
        """Maneja las teclas en la selección de jugadores"""
        if event.keysym == "Up":
            self.current_menu_index = (self.current_menu_index - 1) % len(self.menu_options)
            self.update_menu_display()
        elif event.keysym == "Down":
            self.current_menu_index = (self.current_menu_index + 1) % len(self.menu_options)
            self.update_menu_display()
        elif event.keysym == "Return":
            self.select_player_option()
    
    def handle_instructions_keys(self, event):
        """Maneja las teclas en las instrucciones"""
        if event.keysym == "Return":
            self.game.state_machine.transition_to(GameState.MENU)
            self.create_main_menu()
    
    def handle_game_keys(self, event):
        """Maneja las teclas durante el juego"""
        if event.keysym == "Left":
            available_count = len(self.game.get_available_letters_display())
            self.current_letter_index = (self.current_letter_index - 1) % available_count
            self.update_letter_selection()
        elif event.keysym == "Right":
            available_count = len(self.game.get_available_letters_display())
            self.current_letter_index = (self.current_letter_index + 1) % available_count
            self.update_letter_selection()
        elif event.keysym == "Up":
            self.current_position = (self.current_position - 1) % self.max_word_length
            self.update_word_display()
        elif event.keysym == "Down":
            self.current_position = (self.current_position + 1) % self.max_word_length
            self.update_word_display()
        elif event.keysym == "Return":
            # Enter para seleccionar/colocar letra
            self.place_letter()
        elif event.keysym == "space":
            # Espacio para enviar la palabra
            if any(self.word_positions):  # Si hay letras en la palabra
                self.submit_current_word()
        elif event.keysym == "BackSpace":
            # Backspace para borrar la letra actual
            self.remove_current_letter()
        elif event.keysym == "Escape":
            self.stop_visual_timer()
            self.game.reset_game()
            self.create_main_menu()
    
    def select_menu_option(self):
        """Selecciona una opción del menú principal"""
        option = self.menu_options[self.current_menu_index]
        
        if option == "Jugar":
            self.game.state_machine.transition_to(GameState.PLAYER_SELECTION)
            self.create_player_selection()
        elif option == "Instrucciones":
            self.game.state_machine.transition_to(GameState.INSTRUCTIONS)
            self.create_instructions()
        elif option == "Salir":
            self.root.quit()
    
    def select_player_option(self):
        """Selecciona una opción de jugadores"""
        option = self.menu_options[self.current_menu_index]
        
        if option == "1 Jugador":
            self.game.num_players = 1
            self.start_game()
        elif option == "2 Jugadores":
            self.game.num_players = 2
            self.start_game()
        elif option == "Volver":
            self.game.state_machine.transition_to(GameState.MENU)
            self.create_main_menu()
    
    def start_game(self):
        """Inicia el juego"""
        self.game.state_machine.transition_to(GameState.GAME_SETUP)
        self.game.generate_random_letters()
        self.game.state_machine.transition_to(GameState.PLAYER1_TURN)
        self.create_game_screen()
    
    def bind_events(self):
        """Vincula los eventos de teclado"""
        self.root.bind("<Key>", self.handle_key_event)
        self.root.focus_set()
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()

# Crear y ejecutar la aplicación
if __name__ == "__main__":
    app = WordCraftGUI()
    app.run()
