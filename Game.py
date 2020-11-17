import pygame
import random
from os import path

pygame.init()
pygame.mixer.init()

# Dados gerais do jogo.
TITULO = 'Climbing Tower'
WIDTH = 700 # Largura da tela
HEIGHT = 650 # Altura da tela
TILE_SIZE = 40 # Tamanho de cada tile
PLAYER_WIDTH = TILE_SIZE
PLAYER_HEIGHT = int(TILE_SIZE * 1.5)
FPS = 60 # Frames por segundo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITULO)

#Define as Imagens
img_dir = path.join(path.dirname(__file__), 'img')
BACKGROUND_IMG = 'background_img'
PLAYER_IMG = 'player_img'
BLOCK = 'block'
FONT = 'font'

#Música de Fundo
pygame.mixer.music.load('Mario.mp3')
pygame.mixer.music.set_volume(0.03)
pygame.mixer.music.play(loops=-1)

# Define a aceleração da gravidade
GRAVITY = 3
# Define a velocidade inicial no pulo
JUMP_SIZE = TILE_SIZE
# Define a velocidade em x
SPEED_X = 10
#Começa o jogo com 6 blocos
INITIAL_BLOCKS = 8

# Define estados possíveis do jogador
STILL = 0
JUMPING = 1
FALLING = 2

#perg_jogador = input("Qual modalidae deseja jogar? Falso(F), Médio(M) ou Difícil(D): ")


# Class que representa os blocos do cenário
class Tile(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, tile_img, x, y,speedy):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Aumenta o tamanho do tile.
        tile_img = pygame.transform.scale(tile_img, (100, 20))

        # Define a imagem do tile.
        self.image = tile_img
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Posiciona o tile
        self.rect.x =  x
        self.rect.y =  y
        self.speedy = speedy

    def update(self):
        self.rect.y += self.speedy

# Classe Jogador que representa o herói
class Player(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, player_img,blocks):

        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Define estado atual
        # Usamos o estado para decidir se o jogador pode ou não pular
        self.state = STILL

        # Ajusta o tamanho da imagem
        player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

        # Define a imagem do sprite. Nesse exemplo vamos usar uma imagem estática (não teremos animação durante o pulo)
        self.image = player_img

        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Guarda o grupo de blocos para tratar as colisões
        self.blocks = blocks

        # Posiciona o personagem
        self.rect.x = WIDTH / 2
        self.rect.bottom = HEIGHT

        # Metodo que atualiza a posição do personagem
        self.speedx = 0
        self.speedy = 0

    def update(self):
        # Vamos tratar os movimentos de maneira independente.
        # Primeiro tentamos andar no eixo y e depois no x.

        # Tenta andar em y
        # Atualiza a velocidade aplicando a aceleração da gravidade
        self.speedy += GRAVITY
        # Atualiza o estado para caindo
        if self.speedy > 0:
            self.state = FALLING
        # Atualiza a posição y
        self.rect.y += self.speedy
        # Se colidiu com algum bloco, volta para o ponto antes da colisão
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        # Corrige a posição do personagem para antes da colisão
        for collision in collisions:
            # Estava indo para baixo
            if self.speedy > 0:
                self.rect.bottom = collision.rect.top
                # Se colidiu com algo, para de cair
                self.speedy = 0
                # Atualiza o estado para parado
                self.state = STILL
            # Estava indo para cima
            elif self.speedy < 0:
                self.rect.top = collision.rect.bottom
                # Se colidiu com algo, para de cair
                self.speedy = 0
                # Atualiza o estado para parado
                self.state = STILL

        # Tenta andar em x
        self.rect.x += self.speedx
        # Corrige a posição caso tenha passado do tamanho da janela
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH - 1
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speedy = 0
            self.state =STILL
        # Se colidiu com algum bloco, volta para o ponto antes da colisão
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        # Corrige a posição do personagem para antes da colisão
        for collision in collisions:
            # Estava indo para a direita
            if self.speedx > 0:
                self.rect.right = collision.rect.left
            # Estava indo para a esquerda
            elif self.speedx < 0:
                self.rect.left = collision.rect.right

    # Método que faz o personagem pular
    def jump(self):
        # Só pode pular se ainda não estiver pulando ou caindo
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING


# Carrega todos os assets de uma vez.
def load_assets(img_dir):
    assets = {}
    assets[PLAYER_IMG] = pygame.image.load(path.join(img_dir, 'hero.png')).convert_alpha()
    assets[BLOCK] = pygame.image.load(path.join(img_dir, 'Plataforma.png')).convert()
    assets[BACKGROUND_IMG] = pygame.image.load(path.join(img_dir, 'trump.png')).convert()
    assets[FONT] = pygame.font.Font(path.join(img_dir, 'font.ttf'), 30)
    return assets

def game_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega assets
    assets = load_assets(img_dir)

    # Cria um grupo de todos os sprites.
    all_sprites = pygame.sprite.Group()

    # Esses sprites vão andar junto com o mundo (fundo)
    world_sprites = pygame.sprite.Group()

    # Cria um grupo somente com os sprites de bloco.
    blocks = pygame.sprite.Group()

    # Carrega o fundo do jogo
    background = assets[BACKGROUND_IMG]
    # Redimensiona o fundo   
    background = pygame.transform.scale(background, (700, 650))
    background_rect = background.get_rect()

    # Cria Sprite do jogador
    player = Player(assets[PLAYER_IMG], world_sprites)
    all_sprites.add(player)

    #Lista das posições dos tiles em x
    lista_x = [40, 100, 200, 300, 400, 500, 600]
    lista_y = [-100,-140,-180,-220,-260,-300,-340,-380]
    
    #Velocidade inicial das plataformas
    speed_tile = 1

    # Cria tiles de acordo com o mapa
    for i in range(INITIAL_BLOCKS):
        block_x = random.choice(lista_x) + random.randint(-30,30)
        block_y = random.randint(0, HEIGHT)
        block = Tile(assets[BLOCK], block_x, block_y,speed_tile)
        world_sprites.add(block)
        # Adiciona também no grupo de todos os sprites para serem atualizados e desenhados
        all_sprites.add(block)

    PLAYING = 0
    DONE = 1
    state = PLAYING

    while state != DONE:
        #se o player passar a altura maxima da tela ele volta para o começo
        #porem os tiles irão descer mais rápido
        if player.rect.y < -10:
            player.rect.y = 600
            speed_tile += 0.5
            for block in world_sprites:
                block.kill ()
                block_x = random.choice(lista_x) + random.randint(-30,30)
                block_y = random.choice(lista_y) + random.randint(-30,30)
                new_block = Tile(assets[BLOCK], block_x, block_y, speed_tile)
                all_sprites.add(new_block)
                world_sprites.add(new_block)

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
                    player.speedx -= SPEED_X
                elif event.key == pygame.K_RIGHT:
                    player.speedx += SPEED_X
                elif event.key == pygame.K_UP:
                    player.jump()

            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_LEFT:
                    player.speedx += SPEED_X
                elif event.key == pygame.K_RIGHT:
                    player.speedx -= SPEED_X

        # Verifica se algum bloco saiu da janela
        for block in world_sprites:
            if block.rect.top > HEIGHT:
                # Destrói o bloco e cria um novo no final da tela
                block.kill()
                block_x = random.choice(lista_x) + random.randint(-30,30)
                block_y = random.randint(-400, 200)
                new_block = Tile(assets[BLOCK], block_x, block_y, speed_tile)
                all_sprites.add(new_block)
                world_sprites.add(new_block)
        
        screen.blit(background, background_rect)
        all_sprites.update()
        all_sprites.draw(screen)

        #Quando o player atingir uma certa velocidade máxima o jogo encerra e ele vence
        if speed_tile >= 3:
            text = assets['font'].render('Você ganhou, parabéns!', True, (255, 255, 0))
            posição = text.get_rect()
            posição.midtop = (350, 325)
            screen.fill((50,25,75))
            screen.blit(text, posição)
            block.kill()
            #Fechar a janela do jogo depois de pressionar qualquer tecla
            if event.key == pygame.K_SPACE:
                pygame.quit()
        
        all_sprites.draw(screen)
        pygame.display.flip()
# Comando para evitar travamentos.
try:
    game_screen(screen)
finally:
    pygame.quit()