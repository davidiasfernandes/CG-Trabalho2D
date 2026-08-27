import pygame
from Plataforma import Plataforma
from Margem import Margem
from Sapo import Sapo


LARGURA, ALTURA = 1500, 750
JUMP_SPEED = 5
pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))

clock = pygame.time.Clock()

fonte = pygame.font.Font(None, 30)

a = 750
b = 650

vitoria_regia = Plataforma(a, b)
margem1 = Margem(0, 0)
margem2 = Margem(1300, 0)

carregando_pulo = False
jump_count = 0
rodando = True
player = Sapo(720,625)

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
        player.x = 720
        player.y = 625
    if carregando_pulo:
        jump_count += 7 * JUMP_SPEED
    
   
    player.y -= jump_force

    margem1.desenhar_margem(tela, (44, 85, 30), margem1.x, margem1.x, (44, 60, 30))
    margem2.desenhar_margem(tela, (44, 85, 30), margem2.x, margem2.y, (44, 60, 30))
    vitoria_regia.desenhar_plat(tela, 750, 650, 40, (41, 145, 53))
    vitoria_regia.desenhar_plat(tela, 750, 375, 40, (41, 145, 53))
    vitoria_regia.desenhar_plat(tela, 750, 100, 40, (41, 145, 53))

    texto = fonte.render("x", True, (255, 255, 255))
    tela.blit(texto, (player.x + 25, player.y -jump_count +15))

    player.desenhar_sap(tela)
    
    pygame.display.flip() 
    clock.tick(60)

pygame.quit()
