import pygame
from os import path
from config import WIDHT, HEIGHT, TILE_WIDHT, TILE_HEIGHT, PLAYER_WIDTH,PLAYER_HEIGHT

#Define as Imagens
img_dir = path.join(path.dirname(__file__), 'img')
BACKGROUND_IMG = 'background_img'
PLAYER_IMG = 'player_img'
TILE = 'tile'
SPIKE1_IMG = 'spike'

#Carrega as imagens

def load_assets():
    assets = {}
    assets[TILE] = pygame.image.load(path.join(img_dir, 'Plataforma.png')).convert()
    assets[TILE] = pygame.transform.scale(assets[TILE], (100,40))
    assets[PLAYER_IMG] = pygame.image.load(path.join(img_dir, 'hero.png'))
    assets[PLAYER_IMG] = pygame.transform.scale(assets['player_img'], (PLAYER_WIDTH, PLAYER_HEIGHT))
    assets[SPIKE1_IMG] = pygame.image.load(path.join(img_dir, 'spike1.png')).convert()
    assets[SPIKE1_IMG] = pygame.transform.scale(assets['spike'], (10, 40))
    assets[BACKGROUND_IMG] = pygame.image.load(path.join(img_dir, 'montanhas.png')).convert()    
    return assets