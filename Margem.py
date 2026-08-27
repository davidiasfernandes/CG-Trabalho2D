import random
class Margem:
    
    def __init__(self, x, y):
            self.x = x
            self.y = y

    def desenhar_margem(self, tela, cor,  x, y, cor2):
        if (x == 0):
            x2 = random.randint(5, 195)
            y2 = random.randint(1305, 1495)
            for x in range(202):
                print(x)
                for y in range (751):
                    tela.set_at((x, y), cor)
                    tela.set_at((x2, y2), cor2)
                 
            
        if (x == 1300):
            x2 = random.randint(5, 195)
            y2 = random.randint(1305, 1495)
            for i in range(200):
                for n in range (751):
                    tela.set_at((x+i, y+n), cor)