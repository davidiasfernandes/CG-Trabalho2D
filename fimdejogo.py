import pygame
from Requires.Functions import dda, desenhar_poligono, desenhar_elipse, flood_fill_iterativo

pygame.init()

LARGURA, ALTURA = 1500, 750
tela_final = pygame.display.set_mode((LARGURA, ALTURA))

def desenhar_tela_final():
    tela_final.fill((0, 125, 255))


    fonte_titulo = pygame.font.Font("./Assets/Fonte-Pixel.ttf", 67)
    fonte_texto = pygame.font.Font("./Assets/Fonte-Pixel.ttf", 36)
    superficie_titulo = fonte_titulo.render("Fim de Jogo", True, (255, 255, 255))
    superficie_texto = fonte_texto.render("Clique \"Esc\" para voltar ao menu.", True, (255, 255, 255))

    desenhar_poligono(tela_final, [((LARGURA - superficie_titulo.get_width()) // 2, ALTURA // 4), ((LARGURA + superficie_titulo.get_width()) // 2, ALTURA // 4), ((LARGURA + superficie_titulo.get_width()) // 2, ALTURA // 4 + superficie_titulo.get_height()), ((LARGURA - superficie_titulo.get_width()) // 2, ALTURA // 4 + superficie_titulo.get_height())], (255, 125, 25))
    flood_fill_iterativo(tela_final, (LARGURA - superficie_titulo.get_width()) // 2 + 1, ALTURA // 4 + 1, (255, 125, 25), (255, 125, 25))

    tela_final.blit(superficie_titulo, ((LARGURA - superficie_titulo.get_width()) // 2, ALTURA // 4))
    tela_final.blit(superficie_texto, ((LARGURA - superficie_texto.get_width()) // 2, ALTURA // 2))

    dda(tela_final, LARGURA // 5, ALTURA - 400, LARGURA // 5.2, 620, (0, 0, 0))
    dda(tela_final, LARGURA // 6, ALTURA - 450, LARGURA // 5.1, 650, (0, 0, 0))
    dda(tela_final, LARGURA // 5.5, ALTURA - 400, LARGURA // 5.4, 600, (0, 0, 0))

    desenhar_elipse(tela_final, LARGURA // 5, ALTURA - 400, 35, 50, (255, 255, 0))
    desenhar_elipse(tela_final, LARGURA // 6, ALTURA - 450, 35, 50, (255, 0, 0))
    desenhar_elipse(tela_final, LARGURA // 5.5, ALTURA - 400, 35, 50, (0, 255, 0))

pygame.display.flip()