import pygame
from Cores import MARGEM


class Margem:
    largura = 400
    altura = 750
    cor = MARGEM

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.superficie = pygame.Surface((Margem.largura, Margem.altura))

    def draw(self):
        self.superficie.fill(Margem.cor)