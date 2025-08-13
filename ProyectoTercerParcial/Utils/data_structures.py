import json
import requests
from enum import Enum

class TrieNode:
    """Nodo para el árbol Trie"""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word = None

class Trie:
    """Implementación del árbol Trie para búsqueda eficiente de palabras"""
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """Inserta una palabra en el Trie"""
        node = self.root
        for char in word.upper():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.word = word.upper()
    
    def search(self, word):
        """Busca si una palabra existe en el Trie"""
        node = self.root
        for char in word.upper():
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    
    def starts_with(self, prefix):
        """Verifica si existe alguna palabra que comience con el prefijo dado"""
        node = self.root
        for char in prefix.upper():
            if char not in node.children:
                return False
            node = node.children[char]
        return True

class GameState(Enum):
    """Estados del juego usando máquina de estados finito"""
    MENU = "menu"
    PLAYER_SELECTION = "player_selection"
    GAME_SETUP = "game_setup"
    PLAYER1_TURN = "player1_turn"
    PLAYER2_TURN = "player2_turn"
    WORD_INPUT = "word_input"
    WORD_VALIDATION = "word_validation"
    SCORE_UPDATE = "score_update"
    GAME_OVER = "game_over"
    INSTRUCTIONS = "instructions"

class GameStateMachine:
    """Máquina de estados finito para manejar el flujo del juego"""
    def __init__(self):
        self.current_state = GameState.MENU
        self.transitions = {
            GameState.MENU: [GameState.PLAYER_SELECTION, GameState.INSTRUCTIONS],
            GameState.PLAYER_SELECTION: [GameState.GAME_SETUP, GameState.MENU],
            GameState.GAME_SETUP: [GameState.PLAYER1_TURN],
            GameState.PLAYER1_TURN: [GameState.WORD_INPUT, GameState.PLAYER2_TURN, GameState.GAME_OVER],
            GameState.PLAYER2_TURN: [GameState.WORD_INPUT, GameState.PLAYER1_TURN, GameState.GAME_OVER],
            GameState.WORD_INPUT: [GameState.WORD_VALIDATION],
            GameState.WORD_VALIDATION: [GameState.SCORE_UPDATE, GameState.WORD_INPUT],
            GameState.SCORE_UPDATE: [GameState.PLAYER1_TURN, GameState.PLAYER2_TURN, GameState.GAME_OVER],
            GameState.GAME_OVER: [GameState.MENU],
            GameState.INSTRUCTIONS: [GameState.MENU]
        }
    
    def can_transition_to(self, new_state):
        """Verifica si es posible transicionar al nuevo estado"""
        return new_state in self.transitions.get(self.current_state, [])
    
    def transition_to(self, new_state):
        """Realiza la transición al nuevo estado si es válida"""
        if self.can_transition_to(new_state):
            self.current_state = new_state
            return True
        return False
    
    def get_current_state(self):
        """Retorna el estado actual"""
        return self.current_state

class WordDictionary:
    """Manejo del diccionario de palabras usando únicamente API de la RAE"""
    def __init__(self, json_path=None):
        self.trie = Trie()
        self.validated_words = set()
        self.invalid_words = set()
    
    def is_valid_word(self, word):
        """Verifica si una palabra es válida usando únicamente la API de RAE"""
        word = word.upper().strip()
        
        # Solo palabras de exactamente 4 letras
        if len(word) != 4:
            return False
        
        # Verificar en cache local primero (para evitar llamadas repetidas a la API)
        if word in self.validated_words:
            return True
        if word in self.invalid_words:
            return False
        
        try:
            # API de RAE libre
            url = f"https://rae-api.com/api/words/{word.lower()}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                # La palabra existe en la RAE
                data = response.json()
                if data:  # Si retorna datos, la palabra es válida
                    self.validated_words.add(word)
                    self.trie.insert(word)
                    return True
            elif response.status_code == 404:
                # Palabra no encontrada
                self.invalid_words.add(word)
                return False
            else:
                # Otro error, rechazar palabra
                self.invalid_words.add(word)
                return False
                
        except (requests.exceptions.RequestException, requests.exceptions.Timeout, Exception) as e:
            # Si hay error con la API, rechazar la palabra por seguridad
            self.invalid_words.add(word)
            return False
    
    def has_prefix(self, prefix):
        """Verifica si existe alguna palabra con el prefijo dado"""
        return self.trie.starts_with(prefix)
    
    def get_word_definition(self, word):
        """Función auxiliar para obtener definición de una palabra (para testing)"""
        url = f"https://rae-api.com/api/words/{word.lower()}"
        response = requests.get(url)
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            return None
        return response.json()

def calculate_word_score(word, letter_values=None):
    """Calcula el puntaje de una palabra basado en los valores de las letras"""
    if letter_values is None:
        # Valores por defecto basados en frecuencia de letras en español
        letter_values = {
            'A': 1, 'E': 1, 'I': 1, 'O': 1, 'U': 1,
            'L': 1, 'N': 1, 'R': 1, 'S': 1, 'T': 1,
            'C': 3, 'D': 2, 'G': 2, 'M': 3, 'B': 3,
            'F': 4, 'H': 4, 'P': 3, 'V': 4, 'Y': 4,
            'J': 8, 'K': 5, 'Q': 5, 'W': 8, 'X': 8, 'Z': 10
        }
    
    score = 0
    for letter in word.upper():
        score += letter_values.get(letter, 1)
    
    # Bonus por longitud de palabra
    if len(word) >= 6:
        score += 10
    elif len(word) >= 4:
        score += 5
    
    return score
