from Cores import VERDE_MUSGO
import random
SPEED = 3
RAIO = 40
class Plataforma:
    raio = RAIO
    cor = VERDE_MUSGO
    speed = SPEED

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = random.randint(0,1)

        
    def desenhar_plat(self, tela, a, b, raio, cor):
        for x in range (a - raio, a + raio + 1):
            for y in range (b - raio, b + raio + 1):

                distancia = (x - a) ** 2 + (y - b) ** 2

                if distancia <= raio ** 2:
                    tela.set_at((x,y), cor)

    def draw (self, tela):
        for a in range(int(self.x - Plataforma.raio), int(self.x + Plataforma.raio + 1)):
            for b in range (int(self.y - Plataforma.raio), int(self.y + Plataforma.raio + 1)):

                if ((a - self.x)**2) + ((b -self.y)**2) <= Plataforma.raio**2:
                    tela.set_at((a,b), Plataforma.cor)

        
    def change_direction(self, largura):
        if self.direction == 1 and self.x <= 205 + Plataforma.raio:
            self.direction = 0
        elif self.direction == 0 and self.x >= 1295 - Plataforma.raio:
            self.direction = 1
    

    def move_x_asis(self):
        self.change_direction(1500)
        if self.direction == 1:
            self.x -= Plataforma.speed
        elif self.direction == 0:
            self.x += Plataforma.speed
