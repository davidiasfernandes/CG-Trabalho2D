import math

from Requires.Functions import setPixel
import pygame
from Plataforma import RAIO
import Requires.Functions as Functions

ESCALA_MAX = 1.4

class Sapo:

    def __init__(self, x, y, caminho="./Assets/sapo.png", tamanho=90):
        self.x = x
        self.y = y
        self.largura = tamanho
        self.altura = tamanho
        self.imagem = pygame.image.load(caminho)
        self.cache = {}  # (largura, altura) -> lista de pixels
        self.fator = 1.0
        self.y_inicial = y
        self.pulando = False
        self.destino_y = y
        self.plataforma_atual = None
        self.cache_rot = {}

    def obter_rotacionado(self, theta):
        ang = round(math.degrees(theta) / 5) * 5
        if ang in self.cache_rot: return self.cache_rot[ang]
        lado = round(math.hypot(self.largura, self.altura))
        base = {(x, y): cor for x, y, cor in self.obter_pixels(self.largura, self.altura)}
        destino = [(x, y) for y in range(lado) for x in range(lado)]
        centrados = [(x - lado / 2, y - lado / 2) for x, y in destino]
        # rotação inversa: de cada pixel de destino volta ao pixel de origem
        origens = Functions.aplica_transformacao(Functions.rotacao(-math.radians(ang)), centrados)
        resultado = []
        for (x, y), (ox, oy) in zip(destino, origens):
            cor = base.get((round(ox + self.largura / 2), round(oy + self.altura / 2)))
            if cor is not None: resultado.append((x, y, cor))
        self.cache_rot[ang] = resultado
        return resultado

    def desenhar_rotacionado(self, tela, mouse_x, mouse_y):
        cx, cy = self.get_centro()
        theta = math.atan2(mouse_y - cy, mouse_x - cx)
        lado = round(math.hypot(self.largura, self.altura))
        tela_x, tela_y = cx - lado // 2, cy - lado // 3
        tela.lock()
        for x, y, cor in self.obter_rotacionado(theta):
            pos_x, pos_y = tela_x + x, tela_y + y
            if 0 <= pos_x < tela.get_width() and 0 <= pos_y < tela.get_height():
                setPixel(tela, pos_x, pos_y, cor)
        tela.unlock()

        for i in range(9):
            self.obter_pixels(*(round(90 * (1 + 0.05 * i)),) * 2)

    def obter_pixels(self, larg, alt):
        if (larg, alt) not in self.cache:
            self.cache[(larg, alt)] = Functions.escalar_pixels(self.imagem, larg, alt)
        return self.cache[(larg, alt)]
    
    def desenhar_sap(self, tela, camera_y=0):
        larg = round(self.largura * self.fator)
        alt = round(self.altura * self.fator)
        tela.lock()
        # Cresce a partir do centro, então desloca metade do que aumentou
        tela_x = int(self.x) - (larg - self.largura) // 2
        tela_y = int(self.y - camera_y) - (alt - self.altura) // 2
        for x, y, cor in self.obter_pixels(larg, alt):
            pos_x = tela_x + x
            pos_y = tela_y + y
            if 0 <= pos_x < tela.get_width() and 0 <= pos_y < tela.get_height():
                setPixel(tela, pos_x, pos_y, cor)
        tela.unlock()

    def get_centro(self):
        return self.x + self.largura // 2, self.y + self.altura // 2

    def move_alongside(self, plat):
        dx = -plat.speed if plat.direction == 1 else plat.speed
        self.x, self.y = Functions.transladar_ponto(self.x, self.y, dx, 0)

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
        self.y = plat.y - self.altura // 2
        self.x = plat.x - self.largura // 2

    def atualizar_pulo(self):
        if not self.pulando:
            return
        
        if self.y - 8 > self.destino_y:
            dy = -8
        else:
            dy = self.destino_y - self.y
            self.pulando = False

        self.x, self.y = Functions.transladar_ponto(self.x, self.y, 0, dy)

        total = self.y_inicial - self.destino_y
        if self.pulando and total > 0:
            progresso = (self.y_inicial - self.y) / total
            self.fator = round((1 + (ESCALA_MAX - 1) * math.sin(math.pi * progresso)) * 20) / 20
        else:
            self.fator = 1.0