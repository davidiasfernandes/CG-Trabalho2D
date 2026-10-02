import pygame
from Plataforma import RAIO


def escala(sx, sy):
    return [[sx, 0, 0], 
            [0, sy, 0], 
            [0,  0, 1]]

def escalar_pixels(imagem, nova_larg, nova_alt):
    larg, alt = imagem.get_size()
    m = escala(larg / nova_larg, alt / nova_alt)  # inversa da escala: destino -> origem
    pixels = []
    for xd in range(nova_larg):
        for yd in range(nova_alt):
            xo = m[0][0] * xd + m[0][1] * yd + m[0][2]
            yo = m[1][0] * xd + m[1][1] * yd + m[1][2]
            cor = imagem.get_at((int(xo), int(yo)))
            if cor.a > 128:
                pixels.append((xd, yd, tuple(cor)))
    return pixels


class Sapo:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 90
        self.altura = 90
        self.pixels = escalar_pixels(pygame.image.load("./Assets/sapo.png"), self.largura, self.altura)
        self.pulando = False
        self.destino_y = y
        self.plataforma_atual = None

    def desenhar_sap(self, tela, camera_y=0):
        tela_x = int(self.x)
        tela_y = int(self.y - camera_y)
        for x, y, cor in self.pixels:
            pos_x = tela_x + x
            pos_y = tela_y + y
            if 0 <= pos_x < tela.get_width() and 0 <= pos_y < tela.get_height():
                tela.set_at((pos_x, pos_y), cor)

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
            self.destino_y = self.y - forca

    def pousar(self, plat):
        self.pulando = False
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