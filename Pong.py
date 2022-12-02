import pygame
import random

PRETO=0 ,0 ,0
BRANCO=255,255,255
VERDE=0,255,0
VERMELHO=255,0,0

fim=False
tamanho=600,400
tela=pygame.display.set_mode()
tela_retangulo=tela.get_rect()
tempo=pygame.time.Clock()
pygame.display.set_caption("Pong")

class Raquete:
    def __init__(self, tamanho):
        self.imagem=pygame.Surface(tamanho)
        self.imagem.fill(VERDE)
        self.imagem_retangulo=self.imagem.get_rect()
        self.velocidade = 15
        self.imagem_retangulo[0] = 20

    def move(self, x, y):
        self.imagem_retangulo[0] += x * self.velocidade
        self.imagem_retangulo[1] += y * self.velocidade

    def atualiza(self, tecla):
        if tecla[pygame.K_UP]:
            self.move(0, -1)
        if tecla[pygame.K_DOWN]:
            self.move(0, 1)
        self.imagem_retangulo.clamp_ip(tela_retangulo)

    def realiza(self):
        tela.blit(self.imagem, self.imagem_retangulo)

class Bola:
    def __init__(self, tamanho):
        self.altura, self.largura = tamanho
        self.imagem=pygame.Surface(tamanho)
        self.imagem.fill(VERMELHO)
        self.imagem_retangulo=self.imagem.get_rect()
        self.velocidade = 10
        self.set_bola()

    def aleatorio(self):
        while True:
            num = random.uniform(-1.0, 1.0)
            if num > -.5 and num < 0.5:
                continue
            else:
                return num

    def set_bola(self):
        x = self.aleatorio()
        y = self.aleatorio()
        self.imagem_retangulo.x = tela_retangulo.centerx
        self.imagem_retangulo.y = tela_retangulo.centery
        self.velo = [x, y]
        self.pos = list (tela_retangulo.center)

    def colide_parede(self):
        if self.imagem_retangulo.y < 0 or self.imagem_retangulo.y > tela_retangulo.bottom -self.altura:
            self.velo[1] *= -1
        if self.imagem_retangulo.x < 0 or self.imagem_retangulo.x > tela_retangulo.right - self.largura:
            self.velo[0] *= -1
            if self.imagem_retangulo.x < 0:
                placar1.pontos -= 1
                print("Bateu na parede!")

    def colide_raquete(self, raquete_rect):
        if self.imagem_retangulo.colliderect(raquete_rect):
            self.velo[0] *= -1
            placar1.pontos += 1
            print("Boa, você defendeu!")

    def move(self):
        self.pos[0] += self.velo[0] * self.velocidade
        self.pos[1] += self.velo[1] * self.velocidade
        self.imagem_retangulo.center = self.pos

    def atualiza(self, raquete_rect):
        self.colide_parede()
        self.colide_raquete(raquete_rect)
        self.move()

    def realiza(self):
        tela.blit(self.imagem, self.imagem_retangulo)

class Placar:
    def __init__(self):
        pygame.font.init()
        self.fonte=pygame.font.Font(None, 36)
        self.pontos=10

    def contagem(self):
        self.text=self.fonte.render("Pontos = " + str(self.pontos), 1, (255,255,255))
        self.textpos=self.text.get_rect()
        self.textpos.centerx=tela.get_width() / 2
        tela.blit(self.text, self.textpos)
        tela.blit(tela, (0, 0))

raquete=Raquete((10, 50))
bola=Bola((15, 15))
placar1=Placar()

while not fim:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim=True
    tecla=pygame.key.get_pressed()
    tela.fill(PRETO)
    raquete.realiza()
    bola.realiza()
    raquete.atualiza(tecla)
    bola.atualiza(raquete.imagem_retangulo)
    tempo.tick(30)
    placar1.contagem()
    pygame.display.update()