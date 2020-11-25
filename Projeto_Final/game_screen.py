import pygame
from config import FPS, WIDHT, HEIGHT, BLACK, WINDOW_SIZE, MAP, SPEED_X
from assets import load_assets,BACKGROUND_IMG ,PLAYER_IMG,BLOCK
from clas import Tile, Player

def game_screen(screen):

    # Variável para o ajuste de velocidade

    clock = pygame.time.Clock()

    assets = load_assets()

    # Cria um grupo de todos os sprites.
    all_sprites = pygame.sprite.Group()

    # Esses sprites vão andar junto com o mundo (fundo)
    world_sprites = pygame.sprite.Group()

    # Cria um grupo somente com os sprites de bloco.
    blocks = pygame.sprite.Group()

    # Cria Sprite do jogador
    player = Player(assets[PLAYER_IMG], blocks)
    all_sprites.add(player)

    PLAYING = 0
    DONE = 1
    state = PLAYING

    for column in range(len(MAP)):
        for row in range(len(MAP[column])):
            tile_type = MAP[column][row]
            if tile_type == BLOCK:
                tile = Tile(assets[BLOCK], row, column)
                blocks.add(tile)        
                all_sprites.add(tile)
                world_sprites.add(tile)


    while state != DONE:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():

            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = DONE

            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:

                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_LEFT:
                    for block in blocks:
                        block.speedx += SPEED_X

                elif event.key == pygame.K_RIGHT:
                    for block in blocks:
                        block.speedx -= SPEED_X 

                elif event.key == pygame.K_UP:
                    player.jump()

            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:

                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_LEFT:
                    for block in blocks:
                        block.speedx -= SPEED_X  

                elif event.key == pygame.K_RIGHT:
                    for block in blocks:
                        block.speedx += SPEED_X  


background = assets[BACKGROUND_IMG]
    # Redimensiona o fundo   
background_rect = background.get_rect()

        screen.blit(background, background_rect)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        pygame.display.update()  # Mostra o novo frame para o jogador

    # Comando para evitar travamentos.
    try:
        game_screen(screen)
    finally:
        pygame.quit()