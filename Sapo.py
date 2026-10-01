import pygame

from Plataforma import RAIO


class Sapo:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.pulando = False
        self.plataforma_atual = None
        self.destino_y = y

        self.imagem = pygame.image.load("sapo.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (90, 90))

        # Centro visual
        area_visivel = self.imagem.get_bounding_rect()

        self.centro_x = area_visivel.centerx + 3
        self.centro_y = area_visivel.centery - 10

    def get_centro(self):

        return (
            self.x + self.centro_x,
            self.y + self.centro_y
        )

    def desenhar_sap(self, tela, alpha=255, camera_y=0):

        imagem = self.imagem.copy()
        imagem.set_alpha(alpha)

        tela_y = self.y - camera_y

        tela.blit(
            imagem,
            (
                int(self.x),
                int(tela_y)
            )
        )

    def move_alongside(self, plat):

        if plat.direction == 1:
            self.x -= plat.speed
        else:
            self.x += plat.speed

    def check_underneath(self, plats):

        centro_x, centro_y = self.get_centro()

        for plat in plats:

            distancia = (
                (centro_x - plat.x) ** 2 +
                (centro_y - plat.y) ** 2
            )

            if distancia <= RAIO ** 2:
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

        # Continua usando a posição REAL da plataforma
        self.x = plat.x - self.centro_x
        self.y = plat.y - self.centro_y

    def atualizar_pulo(self):

        if not self.pulando:
            return

        velocidade = 8

        if self.y > self.destino_y:

            self.y -= velocidade

        else:

            self.y = self.destino_y
            self.pulando = False