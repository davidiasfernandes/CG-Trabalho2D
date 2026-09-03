from Cores import VERDE_MUSGO, VERDE_ESCURO
import random
SPEED = 3
RAIO = 40
class Plataforma:
    raio = RAIO
    cor = VERDE_MUSGO
    cor2 = VERDE_ESCURO
    speed = SPEED
    borda = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = random.randint(0,1)

        
    def desenhar_plat(self, tela):
        for x in range (self.x - Plataforma.raio, self.x + Plataforma.raio + 1):
            for y in range (self.y - Plataforma.raio, self.y + Plataforma.raio + 1):

                distancia = (x - self.x) ** 2 + (y - self.y) ** 2

                if distancia < (Plataforma.raio ** 2)- Plataforma.borda:
                    tela.set_at((x,y), Plataforma.cor)
                if (distancia <= Plataforma.raio ** 2) and (distancia > (Plataforma.raio ** 2)- Plataforma.borda):
                    tela.set_at((x,y), Plataforma.cor2)

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
