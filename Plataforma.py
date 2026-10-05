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
        self.x = x
        self.y = y
        self.speed = SPEED
        self.direction = random.randint(0, 1)  # 1 = esquerda, 0 = direita

    def desenhar_plat(self, tela, camera_y=0):

        # A posição física continua sendo self.y.
        # camera_y altera somente onde a plataforma aparece na tela.
        tela_y = self.y - camera_y

        r2 = Plataforma.raio ** 2

        for x in range(
            int(self.x - Plataforma.raio),
            int(self.x + Plataforma.raio + 1)
        ):
            for y in range(
                int(tela_y - Plataforma.raio),
                int(tela_y + Plataforma.raio + 1)
            ):

                distancia = (x - self.x) ** 2 + (y - tela_y) ** 2

                if distancia < r2 - Plataforma.borda:
                    setPixel(tela, x, y, Plataforma.cor)

                elif distancia <= r2:
                    setPixel(tela, x, y, Plataforma.cor2)

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