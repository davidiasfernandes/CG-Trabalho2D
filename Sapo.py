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
        for x in range(self.imagem.get_width()):
            for y in range(self.imagem.get_height()):

                cor = self.imagem.get_at((x, y))

                if cor.a > 0:
                    tela.set_at(
                        (self.x + x, self.y + y),
                        cor
                    )

    def move_alongside(self, plat):
        if plat.direction == 1:
            self.x -= 1 * SPEED
        elif plat.direction == 0:
            self.x += 1 * SPEED

    def check_underneath(self, plats):
        for plat in plats:
            if ((self.x - plat.x) ** 2 + (self.y - plat.y) ** 2) <= (RAIO) ** 2:
                return plat
            
        return None
        
    