import random
import time
import threading
from Utils.data_structures import GameStateMachine, GameState, WordDictionary, calculate_word_score

class WordCraftGame:
    """Clase principal del juego WordCraft"""
    
    def __init__(self):
        self.state_machine = GameStateMachine()
        self.dictionary = WordDictionary()
        
        # Configuración del juego
        self.num_players = 1
        self.current_player = 1
        self.time_limit = 150
        self.available_letters = []
        
        # Datos de los jugadores
        self.player1_score = 0
        self.player2_score = 0
        self.player1_words = []
        self.player2_words = []
        self.player1_time_left = self.time_limit
        self.player2_time_left = self.time_limit
        
        # Estado del input actual
        self.current_word = ""
        self.current_word_letters = []
        self.timer_running = False
        self.game_timer = None
        
        # Flag para detectar nueva ronda
        self.new_round_started = False
        
    def generate_random_letters(self, count=15):
        """Genera letras equilibradas SIN REPETIR para facilitar formar palabras de 4 letras"""
        # Todas las letras del alfabeto español disponibles
        all_possible_letters = list('ABCDEFGHIJKLMNÑOPQRSTUVWXYZ')
        
        # Asegurar que hay suficientes vocales (sin repetir)
        vowels = ['A', 'E', 'I', 'O', 'U']
        consonants = [l for l in all_possible_letters if l not in vowels and l != 'Ñ']
        
        # Seleccionar letras sin repetir
        selected_letters = []
        
        # Agregar al menos 2-3 vocales
        selected_vowels = random.sample(vowels, min(3, len(vowels)))
        selected_letters.extend(selected_vowels)
        
        # Completar con consonantes
        remaining_slots = count - len(selected_letters)
        if remaining_slots > 0:
            available_consonants = [c for c in consonants if c not in selected_letters]
            selected_consonants = random.sample(available_consonants, min(remaining_slots, len(available_consonants)))
            selected_letters.extend(selected_consonants)
        
        # Si aún necesitamos más letras, agregar las restantes vocales
        if len(selected_letters) < count:
            remaining_vowels = [v for v in vowels if v not in selected_letters]
            selected_letters.extend(remaining_vowels)
        
        # Tomar solo la cantidad necesaria
        self.available_letters = selected_letters[:count]
        
        # Mezclar las letras para que no aparezcan ordenadas
        random.shuffle(self.available_letters)
    
    def can_form_word(self, word):
        """Esta función ya no es necesaria pero se mantiene por compatibilidad"""
        return True  # Ahora siempre retorna True ya que no validamos letras disponibles
    
    def use_letters_for_word(self, word):
        """Registra que se usó una palabra pero NO elimina las letras del mazo"""
        # Las letras permanecen disponibles para formar más palabras
        # Solo registramos la palabra como usada
        word = word.upper()
        if self.current_player == 1:
            self.player1_words.append(word)
        else:
            self.player2_words.append(word)
    
    def get_available_letters_display(self):
        """Retorna las letras disponibles para mostrar en la interfaz"""
        return self.available_letters.copy()
    
    def validate_and_score_word(self, word):
        """Valida una palabra y calcula su puntaje"""
        word = word.upper().strip()
        
        if len(word) != 4:
            return False, "La palabra debe tener exactamente 4 letras"
        
        if not self.dictionary.is_valid_word(word):
            return False, "La palabra no está en el diccionario"
        
        # Solo verificar si ya se usó la palabra completa
        all_words = self.player1_words + self.player2_words
        if word in all_words:
            return False, "Esta palabra ya fue usada"
        
        score = calculate_word_score(word)
        return True, score
    
    def submit_word(self, word):
        """Procesa el envío de una palabra por el jugador actual"""
        is_valid, result = self.validate_and_score_word(word)
        
        if is_valid:
            # Agregar puntos al jugador actual
            if self.current_player == 1:
                self.player1_score += result
            else:
                self.player2_score += result
            
            # Registrar la palabra como usada (sin eliminar letras del mazo)
            self.use_letters_for_word(word)
            
            return True, f"¡Palabra válida! +{result} puntos"
        else:
            return False, result
    
    def switch_player(self):
        """Cambia al siguiente jugador"""
        if self.num_players == 2:
            self.current_player = 2 if self.current_player == 1 else 1
            
            # Asegurar que el nuevo jugador tiene tiempo completo
            if self.current_player == 1:
                self.player1_time_left = self.time_limit
                self.state_machine.transition_to(GameState.PLAYER1_TURN)
            else:
                self.player2_time_left = self.time_limit
                self.state_machine.transition_to(GameState.PLAYER2_TURN)
            
            # Generar nuevas letras para el nuevo jugador
            self.generate_random_letters()
            
            # Limpiar palabra actual
            self.current_word = ""
            self.current_word_letters = []
    
    def start_timer(self):
        """Inicia el temporizador para el turno actual"""
        # Detener cualquier temporizador anterior
        self.stop_timer()
        
        self.timer_running = True
        
        def countdown():
            while self.timer_running:
                if self.current_player == 1:
                    if self.player1_time_left > 0:
                        self.player1_time_left -= 1
                else:
                    if self.player2_time_left > 0:
                        self.player2_time_left -= 1
                time.sleep(1)
        
        self.game_timer = threading.Thread(target=countdown)
        self.game_timer.daemon = True
        self.game_timer.start()
    
    def stop_timer(self):
        """Detiene el temporizador"""
        self.timer_running = False
        if self.game_timer and self.game_timer.is_alive():
            self.game_timer.join(timeout=1)  # Esperar hasta 1 segundo para que termine
    
    def end_turn(self):
        """Termina el turno del jugador actual"""
        self.stop_timer()
        
        if self.num_players == 1:
            # En modo de un jugador, el juego termina cuando se acaba el tiempo
            self.state_machine.transition_to(GameState.GAME_OVER)
        elif self.num_players == 2:
            # En modo de dos jugadores, verificar condiciones para terminar el juego
            current_player_time = self.get_current_time_left()
            
            if current_player_time <= 0:
                # El jugador actual se quedó sin tiempo
                if self.current_player == 1:
                    self.player1_time_left = 0
                else:
                    self.player2_time_left = 0
            
            # Verificar si ambos jugadores han jugado (ambos se quedaron sin tiempo)
            if self.player1_time_left <= 0 and self.player2_time_left <= 0:
                # Ambos jugadores terminaron, evaluar resultado
                if self.player1_score == self.player2_score:
                    # Empate: reiniciar con nuevas letras para otra ronda
                    self.start_new_round()
                else:
                    # Hay ganador, terminar juego
                    self.state_machine.transition_to(GameState.GAME_OVER)
            elif current_player_time <= 0:
                # Solo el jugador actual terminó, cambiar al otro jugador
                self.switch_player()
            else:
                # El jugador actual no se quedó sin tiempo, cambiar al siguiente jugador
                self.switch_player()
    
    def get_current_time_left(self):
        """Retorna el tiempo restante del jugador actual"""
        if self.current_player == 1:
            return self.player1_time_left
        else:
            return self.player2_time_left
    
    def start_new_round(self):
        """Inicia una nueva ronda en caso de empate"""
        # Reiniciar tiempo para ambos jugadores
        self.player1_time_left = self.time_limit
        self.player2_time_left = self.time_limit
        
        # Generar nuevas letras
        self.generate_random_letters()
        
        # Reiniciar palabra actual
        self.current_word = ""
        self.current_word_letters = []
        
        # Empezar con el jugador 1
        self.current_player = 1
        self.new_round_started = True
        self.state_machine.transition_to(GameState.PLAYER1_TURN)
    
    def reset_game(self):
        """Reinicia el juego"""
        self.state_machine = GameStateMachine()
        self.player1_score = 0
        self.player2_score = 0
        self.player1_words = []
        self.player2_words = []
        self.player1_time_left = self.time_limit
        self.player2_time_left = self.time_limit
        self.current_player = 1
        self.current_word = ""
        self.current_word_letters = []
        self.available_letters = []
        self.new_round_started = False
        self.stop_timer()
    
    def get_game_summary(self):
        """Retorna un resumen del juego para mostrar al final"""
        summary = {
            'player1_score': self.player1_score,
            'player2_score': self.player2_score,
            'player1_words': self.player1_words,
            'player2_words': self.player2_words,
            'winner': None
        }
        
        if self.num_players == 2:
            if self.player1_score > self.player2_score:
                summary['winner'] = 1
            elif self.player2_score > self.player1_score:
                summary['winner'] = 2
            else:
                summary['winner'] = 'tie'
        
        return summary
