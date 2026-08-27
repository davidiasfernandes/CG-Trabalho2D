import pygame

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