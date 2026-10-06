import random

from Cores import VERDE_MUSGO, VERDE_ESCURO
from Margem import Margem, LARGURA_MARGEM
from Requires.Functions import setPixel

SPEED = 3.5
RAIO = 40


class Plataforma:

    raio = RAIO
    cor = VERDE_MUSGO
    cor2 = VERDE_ESCURO
    borda = 100

    def __init__(self, x, y):
        Plataforma.criar_pixels()
        self.x = x
        self.y = y
        self.speed = SPEED
        self.direction = random.randint(0, 1)  # 1 = esquerda, 0 = direita

    pixels = []

    @classmethod
    def criar_pixels(cls):
        if cls.pixels:
            return

        r2 = cls.raio ** 2

        for px in range(-cls.raio, cls.raio + 1):
            for py in range(-cls.raio, cls.raio + 1):

                distancia = px ** 2 + py ** 2

                if distancia < r2 - cls.borda:
                    cls.pixels.append((px, py, cls.cor))

                elif distancia <= r2:
                    cls.pixels.append((px, py, cls.cor2))

    def desenhar_plat(self, tela, camera_y=0):
        tela_y = self.y - camera_y
        tela.lock()
        # Desenha os pixels já calculados.
        for dx, dy, cor in Plataforma.pixels:
            x = int(self.x + dx)
            y = int(tela_y + dy)
            setPixel(tela, x, y, cor)
        tela.unlock()

    def change_direction(self, largura):

        # Inverte a direção ao encostar nas margens
        if self.direction == 1 and self.x <= LARGURA_MARGEM + 5 + Plataforma.raio:
            self.direction = 0

        elif self.direction == 0 and self.x >= largura - LARGURA_MARGEM - 5 - Plataforma.raio:
            self.direction = 1

    def move_x_asis(self):

        self.change_direction(1500)

        if self.direction == 1:
            self.x -= self.speed
        else:
            self.x += self.speed