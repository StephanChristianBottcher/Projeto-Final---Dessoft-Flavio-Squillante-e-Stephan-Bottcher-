import pygame
from config import WIDHT, HEIGHT, TILE_WIDHT, TILE_HEIGHT, PLAYER_WIDTH,PLAYER_HEIGHT ,GRAVITY, STILL, FALLING,JUMPING,JUMP_SIZE

class Tile(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, image, x, y):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Define a imagem do tile.
        self.image = image

        # Detalhes sobre o posicionamento.

        self.rect = self.image.get_rect()
        self.rect.x = x * 100
        self.rect.y = y * 40
        self.speedx = 0

    def update(self):
        
        # Atualiza a posição x
        self.rect.x += self.speedx   

class Spike1(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, image, x, y):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Define a imagem do tile.
        self.image = image
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        self.rect.x = x * 100
        self.rect.y = y * 40
        self.speedx = 0

    def update(self):

        # Atualiza a posição x
        self.rect.x += self.speedx      

# Classe Jogador que representa o herói
class Player(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, image,blocks,spike1):

        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Define estado atual
        # Usamos o estado para decidir se o jogador pode ou não pular
        self.state = STILL

        # Define a imagem do sprite. Nesse vamos usar uma imagem estática (não teremos animação durante o pulo)
        self.image = image

        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Guarda o grupo de blocos para tratar as colisões
        self.blocks = blocks
        self.spike1 = spike1

        # Posiciona o personagem
        self.rect.x = WIDHT/2
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
            if self.speedy > 0 and self.rect.top < collision.rect.top:
                
                self.rect.bottom = collision.rect.top
                # Se colidiu com algo, para de cair
                self.speedy = 0
                # Atualiza o estado para parado
                self.state = STILL
                break
            # Estava indo para cima
            elif self.speedy < 0:
                #time.sleep(2)
                self.rect.top = collision.rect.bottom
                # Se colidiu com algo, para de cair
                self.speedy = 0
                # Atualiza o estado para parado
                self.state = STILL
                break
        # Corrige a posição caso tenha passado do tamanho da janela
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        # Corrige a posição do personagem para antes da colisão
        for collision in collisions:
            # Estava indo para a direita
            if collision.speedx > 0:
                self.rect.left = collision.rect.right
                break
            # Estava indo para a esquerda
            elif collision.speedx < 0:
                self.rect.right = collision.rect.left
                break
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >= WIDHT:
            self.rect.right = WIDHT - 1
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speedy = 0
            self.state = STILL

    # Método que faz o personagem pular
    def jump(self):
        # Só pode pular se ainda não estiver pulando ou caindo
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING