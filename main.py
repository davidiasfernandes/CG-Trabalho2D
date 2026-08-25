import pygame
from Plataforma import Plataforma
from Margem import Margem

pygame.init()

tela = pygame.display.set_mode((1500, 750))

a = 750
b = 650
vitoria_regia = Plataforma(a, b)
margem1 = Margem(0, 0)
margem2 = Margem(1300, 0)

rodando = True

while rodando:

    for evento in pygame.event.get():

        if (evento.type == pygame.QUIT):
            rodando = False

    tela.fill((41, 101, 190))
    
    margem1.desenhar_margem(tela, (44, 85, 30), margem1.x, margem2.x, (44, 60, 30))
    margem2.desenhar_margem(tela, (44, 85, 30), margem2.x, margem2.y, (44, 60, 30))
    vitoria_regia.desenhar_plat(tela, 750, 650, 40, (41, 145, 53))
    pygame.display.flip() 

pygame.quit()
