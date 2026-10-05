import pygame
from Cores import MARGEM
from Requires.Functions import setPixel
import Requires.Functions as Functions

class Margem:
    largura = 200
    altura = 750
    cor = MARGEM

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.superficie = pygame.Surface((Margem.largura, Margem.altura))
        self.imagem = pygame.image.load("./Assets/pedra.png")
        Functions.escalar_pixels(self.imagem, 25, 25)

    def draw(self):
        Functions.scanline_fill(self.superficie, [(0, 0), (Margem.largura, 0), (Margem.largura, Margem.altura), (0, Margem.altura)], Margem.cor)

    def obter_pixels(self, larg, alt):
            if (larg, alt) not in self.cache:
                self.cache[(larg, alt)] = Functions.escalar_pixels(self.imagem, larg, alt)
            return self.cache[(larg, alt)]
        
    def desenhar_pedra(self, tela, camera_y=0):
        larg = round(self.largura * self.fator)
        alt = round(self.altura * self.fator)
        # Cresce a partir do centro, então desloca metade do que aumentou
        tela_x = int(self.x) - (larg - self.largura) // 2
        tela_y = int(self.y - camera_y) - (alt - self.altura) // 2
        for x, y, cor in self.obter_pixels(larg, alt):
            pos_x = tela_x + x
            pos_y = tela_y + y
            if 0 <= pos_x < tela.get_width() and 0 <= pos_y < tela.get_height():
                setPixel(tela, pos_x, pos_y, cor)