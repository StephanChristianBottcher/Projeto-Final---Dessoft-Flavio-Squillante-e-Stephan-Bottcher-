import pygame
from config import FPS, WIDHT, HEIGHT, BLACK, WINDOW_SIZE, MAP, SPEED_X, BLOCK, SPIKE1
from assets import load_assets,BACKGROUND_IMG ,PLAYER_IMG,TILE,SPIKE1_IMG
from clas import Tile, Player,Spike1

def game_screen(screen):

    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega assets
    assets = load_assets()

    # Cria um grupo de todos os sprites.
    all_sprites = pygame.sprite.Group()

    # Cria um grupo somente com os sprites de bloco.
    blocks = pygame.sprite.Group()

    # Cria um grupo somente com os sprites de spike.
    spike1 = pygame.sprite.Group()


    # Carrega o fundo do jogo
    background = assets[BACKGROUND_IMG]
    # Redimensiona o fundo
    background = pygame.transform.scale(background, WINDOW_SIZE)
    background_rect = background.get_rect()
    
    # Cria Sprite do jogador
    player = Player(assets[PLAYER_IMG], blocks,spike1)
    all_sprites.add(player)

    PLAYING = 0
    DONE = 1
    state = PLAYING

    #Criação dos Tiles e Spikes
    
    for column in range(len(MAP)):
        for row in range(len(MAP[column])):
            tile_type = MAP[column][row]
            if tile_type == BLOCK:
                tile = Tile(assets['tile'], row, column)
                blocks.add(tile)
                all_sprites.add(tile)
            
            if tile_type == SPIKE1:
                tile = Spike1(assets['spike'], row, column)
                spike1.add(tile)        
                all_sprites.add(tile)
    
    while state != DONE:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():

            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state=DONE

            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:

                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_LEFT:    
                    
                    for block in blocks:
                        block.speedx = SPEED_X
                          
                    for spikeo1 in spike1:   
                        spikeo1.speedx = SPEED_X
                     

                elif event.key == pygame.K_RIGHT:
                    for block in blocks:
                        block.speedx = -SPEED_X
                    for spikeo1 in spike1:   
                        spikeo1.speedx = -SPEED_X

                elif event.key == pygame.K_UP:
                    player.jump()

            # Verifica se soltou alguma tecla.

            if event.type == pygame.KEYUP:
                
                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_LEFT:
                    
                    #player.speedx += SPEED_X
                    for block in blocks:
                        block.speedx = 0  
                    for spikeo1 in spike1:   
                        spikeo1.speedx = 0
                          
                    
                elif event.key == pygame.K_RIGHT:
                    
                    #player.speedx -= SPEED_X
                    for block in blocks:
                        block.speedx = 0
                    for spikeo1 in spike1:   
                        spikeo1.speedx = 0
      
        # Verifica a colisão do player com o spike
        spike1_hit = pygame.sprite.spritecollide(player, spike1, False)
        if len(spike1_hit) > 0:
            state = DONE
             
        screen.blit(background, background_rect)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()