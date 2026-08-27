import pygame
from Plataforma import Plataforma
from Margem import Margem


LARGURA, ALTURA = 1500, 750
JUMP_SPEED = 10
pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))

a = 750
b = 650
vitoria_regia = Plataforma(a, b)
margem1 = Margem(0, 0)
margem2 = Margem(1300, 0)
carregando_pulo = False
jump_count = 0
rodando = True
player = [a,b]
while rodando:
    jump_force = 0
   
    for evento in pygame.event.get():

        if (evento.type == pygame.QUIT):
            rodando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            carregando_pulo = True
        elif evento.type == pygame.KEYUP and evento.key == pygame.K_SPACE:
            carregando_pulo = False
            jump_force = jump_count
            jump_count = 0

    tela.fill((41, 101, 190))

    if pygame.key.get_pressed()[pygame.K_0]:
        player = [a,b]
    if carregando_pulo:
        jump_count += 10 * JUMP_SPEED
    
   
    player[1] -= jump_force
    margem1.desenhar_margem(tela, (44, 85, 30), margem1.x, margem1.x, (44, 60, 30))
    margem2.desenhar_margem(tela, (44, 85, 30), margem2.x, margem2.y, (44, 60, 30))
    vitoria_regia.desenhar_plat(tela, 750, 650, 40, (41, 145, 53))
    vitoria_regia.desenhar_plat(tela, 750, 375, 40, (41, 145, 53))
    vitoria_regia.desenhar_plat(tela, 750, 100, 40, (41, 145, 53))
    pygame.draw.circle(tela, (250, 200, 50, 0.1), (750, player[1] -jump_count), 20)
    pygame.draw.circle(tela, (255, 0, 0), player, 20)
    
    pygame.display.flip() 

pygame.quit()
