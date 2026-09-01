


import pygame
from Plataforma import Plataforma
from Margem import Margem
from Sapo import Sapo
from Cores import AZUL_AGUA

def calculate_plats(initial_lenght, initial_height, screen_height, space_between):
    margin = screen_height - initial_height
    intervalo = initial_height - margin
    quantidade = int(intervalo//space_between) + 1

    return [Plataforma(initial_lenght, initial_height - i * space_between) for i in range(quantidade)]
    

LARGURA, ALTURA = 1500, 750
JUMP_SPEED = 8
INITIAL_X, INITIAL_Y = 750, 650


pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
fonte = pygame.font.Font(None, 30)

plats = calculate_plats(INITIAL_X, INITIAL_Y, ALTURA, 275)
plats[0].direction = -1
margem1 = Margem(0, 0)
margem2 = Margem(LARGURA-200, 0)

margem1.draw()
margem2.draw()
player = Sapo(INITIAL_X -30, INITIAL_Y - 25)


carregando_pulo = False
jump_count = 0
rodando = True


while rodando:
    jump_force = 0
   
    for evento in pygame.event.get():

        if (evento.type == pygame.QUIT):
            rodando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            carregando_pulo = True
        elif evento.type == pygame.KEYUP and evento.key == pygame.K_SPACE:
            carregando_pulo = False
            player.y -= jump_count
            jump_count = 0

    tela.fill(AZUL_AGUA)

    if pygame.key.get_pressed()[pygame.K_0]:
        player.x = 720
        player.y = 625


    if carregando_pulo:
        jump_count += 1 * JUMP_SPEED
        tela.blit(texto, (player.x, player.y -jump_count))
    print(margem1.superficie)
   


    tela.blit(margem1.superficie, (margem1.x, margem1.y))
    tela.blit(margem2.superficie, (margem2.x, margem2.y))
    for plat in plats:
        plat.draw(tela)
        plat.move_x_asis()
    
    under = player.check_underneath(plats)
    if under != None:
        player.move_alongside(under)
    else:
        player.x = INITIAL_X -30
        player.y = INITIAL_Y - 25

    texto = fonte.render("x", True, (255, 255, 255))
    

    player.desenhar_sap(tela)
    
    pygame.display.flip() 
    clock.tick(60)

pygame.quit()

