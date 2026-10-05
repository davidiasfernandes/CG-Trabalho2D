import pygame
from Cores import MARGEM
from Requires.Functions import setPixel
import Requires.Functions as Functions

LARGURA_MARGEM = 300
ALTURA_MARGEM = 750

class Margem:
    cor = MARGEM

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.superficie = pygame.Surface((LARGURA_MARGEM, ALTURA_MARGEM))
        self.imagem = pygame.image.load("./Assets/pedra.png")
        Functions.escalar_pixels(self.imagem, 25, 25)

    def draw(self):
        Functions.scanline_fill(self.superficie, [(0, 0), (LARGURA_MARGEM, 0), (LARGURA_MARGEM, ALTURA_MARGEM), (0, ALTURA_MARGEM)], MARGEM)

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