class Plataforma:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def desenhar_plat(self, tela, a, b, raio, cor):
        for x in range (a - raio, a + raio + 1):
            for y in range (b - raio, b + raio + 1):

                distancia = (x - a) ** 2 + (y - b) ** 2

                if distancia <= raio ** 2:
                    tela.set_at((x,y), cor)
