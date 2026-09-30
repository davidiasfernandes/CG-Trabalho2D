import random
from Cores import VERDE_MUSGO, VERDE_ESCURO

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

    def desenhar_plat(self, tela):
        # Círculo pixel a pixel: miolo verde claro e anel externo verde escuro (borda)
        r2 = Plataforma.raio ** 2
        for x in range(int(self.x - Plataforma.raio), int(self.x + Plataforma.raio + 1)):
            for y in range(int(self.y - Plataforma.raio), int(self.y + Plataforma.raio + 1)):
                distancia = (x - self.x) ** 2 + (y - self.y) ** 2
                if distancia < r2 - Plataforma.borda:
                    tela.set_at((x, y), Plataforma.cor)
                elif distancia <= r2:
                    tela.set_at((x, y), Plataforma.cor2)

    def change_direction(self, largura):
        # Inverte a direção ao encostar nas margens (200px de cada lado)
        if self.direction == 1 and self.x <= 205 + Plataforma.raio:
            self.direction = 0
        elif self.direction == 0 and self.x >= 1295 - Plataforma.raio:
            self.direction = 1

    def move_x_asis(self):
        self.change_direction(1500)
        if self.direction == 1:
            self.x -= self.speed
        else:
            self.x += self.speed