import pygame
import random
from Cores import MARGEM
class Margem:

    largura = 200
    altura = 750
    cor = MARGEM

    def __init__(self, x, y):
            self.x = x
            self.y = y
            self.superficie = pygame.Surface((Margem.largura, Margem.altura))

    def draw(self):
        for i in range (Margem.largura):
            for n in range(Margem.altura):
                self.superficie.set_at((i, n), Margem.cor)
