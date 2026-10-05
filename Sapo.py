import math

from Requires.Functions import setPixel
import pygame
from Plataforma import RAIO
import Requires.Functions as Functions

ESCALA_MAX = 1.4

class Sapo:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 90
        self.altura = 90
        self.imagem = pygame.image.load("./Assets/sapo.png")
        self.cache = {}  # (largura, altura) -> lista de pixels
        self.fator = 1.0
        self.y_inicial = y
        self.pulando = False
        self.destino_y = y
        self.plataforma_atual = None

    def obter_pixels(self, larg, alt):
        if (larg, alt) not in self.cache:
            self.cache[(larg, alt)] = Functions.escalar_pixels(self.imagem, larg, alt)
        return self.cache[(larg, alt)]
    
    def desenhar_sap(self, tela, camera_y=0):
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

    def get_centro(self):
        return self.x + self.largura // 2, self.y + self.altura // 2

    def move_alongside(self, plat):
        if plat.direction == 1:
            self.x -= plat.speed
        else:
            self.x += plat.speed

    def check_underneath(self, plats):
        centro_x, centro_y = self.get_centro()
        for plat in plats:
            if (centro_x - plat.x) ** 2 + (centro_y - plat.y) ** 2 <= RAIO ** 2:
                return plat
        return None

    def pular(self, forca):
        if not self.pulando:
            self.pulando = True
            self.plataforma_atual = None
            self.y_inicial = self.y
            self.destino_y = self.y - forca

    def pousar(self, plat):
        self.pulando = False
        self.fator = 1.0
        self.plataforma_atual = plat
        self.x = plat.x - self.largura // 2
        self.y = plat.y - self.altura // 2

    def atualizar_pulo(self):
        if not self.pulando:
            return
        if self.y > self.destino_y:
            self.y -= 8
        else:
            self.y = self.destino_y
            self.pulando = False
        total = self.y_inicial - self.destino_y
        if self.pulando and total > 0:
            progresso = (self.y_inicial - self.y) / total
            self.fator = 1 + (ESCALA_MAX - 1) * math.sin(math.pi * progresso)
        else:
            self.fator = 1.0