import pygame
from pygame.locals import *
import sys
import random
from pygame import mixer
import pygame_menu

pygame.init()

#Váriaveis
vetor = pygame.math.Vector2
altura = 406
largura = 700
velocidade = 0.3
friccao = -0.10
fps = 60
fps_clock = pygame.time.Clock()
count = 0

#Criação da tela
display = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Fruit Attack")

#Imagens das animações do personagem lado direito
personagem_d = [pygame.image.load("jogador/Player_Sprite_R.png"), pygame.image.load("jogador/Player_Sprite2_R.png"),
                pygame.image.load("jogador/Player_Sprite3_R.png"), pygame.image.load("jogador/Player_Sprite4_R.png"),
                pygame.image.load("jogador/Player_Sprite5_R.png"), pygame.image.load("jogador/Player_Sprite6_R.png"),
                pygame.image.load("jogador/Player_Sprite_R.png")]

#Imagens das animações do personagem lado esquerdo
personagem_e = [pygame.image.load("jogador/Player_Sprite_L.png"), pygame.image.load("jogador/Player_Sprite2_L.png"),
                pygame.image.load("jogador/Player_Sprite3_L.png"), pygame.image.load("jogador/Player_Sprite4_L.png"),
                pygame.image.load("jogador/Player_Sprite5_L.png"), pygame.image.load("jogador/Player_Sprite6_L.png"),
                pygame.image.load("jogador/Player_Sprite_L.png")]

#Imagens das animações de ataques lado direito
ataque_d = [pygame.image.load("jogador/Player_Sprite_R.png"), pygame.image.load("jogador/Player_Attack_R.png"),
            pygame.image.load("jogador/Player_Attack2_R.png"), pygame.image.load("jogador/Player_Attack2_R.png"),
            pygame.image.load("jogador/Player_Attack3_R.png"), pygame.image.load("jogador/Player_Attack3_R.png"),
            pygame.image.load("jogador/Player_Attack4_R.png"), pygame.image.load("jogador/Player_Attack4_R.png"),
            pygame.image.load("jogador/Player_Attack5_R.png"), pygame.image.load("jogador/Player_Attack5_R.png"),
            pygame.image.load("jogador/Player_Sprite_R.png")]

#Imagens das animações de ataques lado esquerdo
ataque_e = [pygame.image.load("jogador/Player_Sprite_L.png"), pygame.image.load("jogador/Player_Attack_L.png"),
            pygame.image.load("jogador/Player_Attack2_L.png"), pygame.image.load("jogador/Player_Attack2_L.png"),
            pygame.image.load("jogador/Player_Attack3_L.png"), pygame.image.load("jogador/Player_Attack3_L.png"),
            pygame.image.load("jogador/Player_Attack4_L.png"), pygame.image.load("jogador/Player_Attack4_L.png"),
            pygame.image.load("jogador/Player_Attack5_L.png"), pygame.image.load("jogador/Player_Attack5_L.png"),
            pygame.image.load("jogador/Player_Sprite_L.png")]

#Classe Background
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("cenario/Background.png")
        self.rectBGimg = self.bgimage.get_rect()
        self.bgY = 0
        self.bgX = 0

    def render(self):
        display.blit(self.bgimage, (self.bgX, self.bgY))

#Classe Ground
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cenario/Ground.png")
        self.rect = self.image.get_rect(center=(350, 390))
        self.bgX1 = 0
        self.bgY1 = 380

    def render(self):
        display.blit(self.image, (self.bgX1, self.bgY1))

#Classe Personagem
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("jogador/Player_Sprite_R.png")
        self.rect = self.image.get_rect()

        # Posição e Direção
        self.vx = 0
        self.pos = vetor((340, 240))
        self.vel = vetor(0, 0)
        self.acc = vetor(0, 0)
        self.direcao = "RIGHT"

        #Pulo e Andamento
        self.pulando = False
        self.andamento = False
        self.frame = 0

        #Combate
        self.ataque = False
        self.ataque_frame = 0

    def movimento(self):

        self.acc = vetor(0, 0.5)

        if abs(self.vel.x) > 0.3:
            self.andamento = True
        else:
            self.andamento = False

        # Movimento do personagem ao usar as teclas
        teclas = pygame.key.get_pressed()
        if teclas[K_LEFT]:
            self.acc.x = -velocidade
        if teclas[K_RIGHT]:
            self.acc.x = velocidade

        self.acc.x += self.vel.x * friccao
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > largura:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = largura

        self.rect.midbottom = self.pos  # Update rect with new pos

    def gravidade(self):
        p = pygame.sprite.spritecollide(personagem, ground_group, False)
        if self.vel.y > 0:
            if p:
                l = p[0]
                if self.pos.y < l.rect.bottom:
                    self.pos.y = l.rect.top + 1
                    self.vel.y = 0
                    self.pulando = False

    def update(self):
        if self.frame > 6:
            self.frame = 0
            return

        #Animações
        if self.pulando == False and self.andamento == True:
            if self.vel.x > 0:
                self.image = personagem_d[self.frame]
                self.direcao = "RIGHT"
            else:
                self.image = personagem_e[self.frame]
                self.direcao = "LEFT"
            self.frame += 1

        if abs(self.vel.x) < 0.2 and self.frame != 0:
            self.frame = 0
            if self.direcao == "RIGHT":
                self.image = personagem_d[self.frame]
            elif self.direcao == "LEFT":
                self.image = personagem_e[self.frame]

    def atacando(self):
        #Ataque volta ao fame base
        if self.ataque_frame > 10:
            self.ataque_frame = 0
            self.ataque = False

        #Verifica a direção correta da animação do ataque
        if self.direcao == "RIGHT":
            self.image = ataque_d[self.ataque_frame]
        elif self.direcao == "LEFT":
            self.correcao()
            self.image = ataque_e[self.ataque_frame]

        self.ataque_frame += 1

    def pulo(self):
        self.rect.x += 1

        #Checagem do personagem no solo
        p = pygame.sprite.spritecollide(self, ground_group, False)
        self.rect.x -= 1
        if p and not self.pulando:
            self.pulando = True
            self.vel.y = -12

    def correcao(self):
        if self.ataque_frame == 1:
            self.pos.x -= 20
        if self.ataque_frame == 10:
            self.pos.x += 20

#Classe Inimigo
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("inimigos/pizza.png")
        self.rect = self.image.get_rect()
        self.pos = vetor(0,0)
        self.vel = vetor(0,0)

        self.direcao = random.randint(0, 1)
        self.vel.x = random.randint(2, 6) / 2

        #Poisição inicial do inimigo
        if self.direcao == 0:
            self.pos.x = 0
            self.pos.y = 335
        if self.direcao == 1:
            self.pos.x = 600
            self.pos.y = 335

    def movimento(self):
        #Mudar de direção ao final da tela
        if self.pos.x >= (largura - 20):
            self.direcao = 1
        elif self.pos.x <= 0:
            self.direcao = 0

        #Update com novos valores
        if self.direcao == 0:
            self.pos.x += self.vel.x
        if self.direcao == 1:
            self.pos.x -= self.vel.x
        self.rect.center = self.pos

    def renderizacao(self):
        self.movimento()
        display.blit(self.image, (self.pos.x, self.pos.y))

personagem = Personagem()
Personagemgroup = pygame.sprite.Group()
inimigo = Inimigo()
background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

#Músicas e sons de efeitos especiais
pygame.mixer.music.load("sons/fundo.wav")
pygame.mixer.music.play(-1)
espada = pygame.mixer.Sound("sons/espada.wav")
pu = pygame.mixer.Sound("sons/pulo.wav")

while True:
    personagem.gravidade()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                personagem.pulo()
                pu.play()
            if event.key == pygame.K_a:
                if personagem.ataque == False:
                    personagem.atacando()
                    personagem.ataque = True
                    espada.play()

    #Funções do personagem
    personagem.update()
    if personagem.ataque == True:
        personagem.atacando()
    personagem.movimento()

    #Cenário
    background.render()
    ground.render()

    #Renderização do personagem
    display.blit(personagem.image, personagem.rect)
    inimigo.renderizacao()
    pygame.display.update()
    menu.mainloop(display)
    #menu()
    fps_clock.tick(fps)