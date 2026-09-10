import pygame
from Plataforma import SPEED, RAIO

class Sapo:


    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.imagem = pygame.image.load("sapo.png").convert_alpha()

        self.imagem = pygame.transform.scale(
            self.imagem,
            (65, 65)
        )

    def desenhar_sap(self, tela):
        for x in range(int(self.imagem.get_width())):
            for y in range(int(self.imagem.get_height())):

                cor = self.imagem.get_at((x, y))

                if cor.a > 0:
                    tela.set_at(
                        (int(self.x + x), int(self.y + y)),
                        cor
                    )

    def move_alongside(self, plat):
        if plat.direction == 1:
            self.x -= 1 * plat.speed
        elif plat.direction == 0:
            self.x += 1 * plat.speed
        print(plat.speed)

    def check_underneath(self, plats):
        for plat in plats:
            if ((self.x - plat.x) ** 2 + (self.y - plat.y) ** 2) <= (RAIO) ** 2:
                return plat
            
        return None
        

    def pular(self, forca):

        if not self.pulando:

            self.pulando = True
            self.plataforma_atual = None

            self.destino_y = self.y - forca

    def pousar(self, plat):
        self.pulando = False
        self.plataforma_atual = plat

    def atualizar_pulo(self):

        if self.pulando:

            velocidade = 8

            if self.y > self.destino_y:

                self.y -= velocidade

                if self.y <= self.destino_y:
                    self.y = self.destino_y
                    self.pulando = False
    