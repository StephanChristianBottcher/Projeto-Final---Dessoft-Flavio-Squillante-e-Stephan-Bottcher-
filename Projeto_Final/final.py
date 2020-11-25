# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
from config import WIDHT, HEIGHT, INIT, GAME, QUIT
from Tela_Inicial import init_screen
from game_screen import game_screen


pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption('Mario')

state = INIT

while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    if state == GAME:
        state = game_screen(window)
    else:
        state = QUIT

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados