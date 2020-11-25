import pygame
from os import path
from config import WIDHT, HEIGHT, TILE_WIDHT, TILE_HEIGHT, PLAYER_WIDTH,PLAYER_HEIGHT

#Define as Imagens
img_dir = path.join(path.dirname(__file__), 'img')
BACKGROUND_IMG = 'background_img'
PLAYER_IMG = 'player_img'
BLOCK = 'block'
FONT = 'font'


def load_assets():
    assets = {}
    assets[BLOCK] = pygame.image.load(path.join(img_dir, 'Plataforma.png')).convert()
    assets[BLOCK] = pygame.transform.scale(assets['block'], (40,TILE_HEIGHT))
    assets[PLAYER_IMG] = pygame.image.load(path.join(img_dir, 'hero.png'))
    assets[PLAYER_IMG] = pygame.transform.scale(assets['player_img'], (PLAYER_WIDTH, PLAYER_HEIGHT))
    assets[BACKGROUND_IMG] = pygame.image.load(path.join(img_dir, 'trump.png')).convert()
    
    return assets