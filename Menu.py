import pygame

from Requires.Functions import desenhar_poligono, flood_fill_iterativo
from Cores import VERDE_MUSGO, VERDE_ESCURO

pygame.init()

# Configuração da janela
LARGURA, ALTURA = 1500, 750
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Menu do Jogo")

clock = pygame.time.Clock()

# 3. Fontes e Cores
# Usamos SysFont com pixel art/arcade estilo padrão, ou None para a fonte padrão
fonte_titulo = pygame.font.Font("./Assets/Fonte-Pixel.ttf", 67)
fonte_botao = pygame.font.Font("./Assets/Fonte-Pixel.ttf", 36)

COR_TEXTO = (255, 255, 255)

# 4. Definição dos Botões (Posição X, Posição Y, Largura, Altura)
LARGURA_BOTAO = 300
ALTURA_BOTAO = 60
X_CENTRO = (LARGURA - LARGURA_BOTAO) // 2

btn_jogar = [(LARGURA/2 -LARGURA_BOTAO / 2, 350), (LARGURA/2 -LARGURA_BOTAO / 2, 350 + ALTURA_BOTAO), (LARGURA/2 + LARGURA_BOTAO / 2, 350 + ALTURA_BOTAO), (LARGURA/2 + LARGURA_BOTAO / 2, 350)]
btn_ajuda = [(LARGURA/2 -LARGURA_BOTAO / 2, 450), (LARGURA/2 -LARGURA_BOTAO / 2, 450 + ALTURA_BOTAO), (LARGURA/2 + LARGURA_BOTAO / 2, 450 + ALTURA_BOTAO), (LARGURA/2 + LARGURA_BOTAO / 2, 450)]
btn_sair = [(LARGURA/2 -LARGURA_BOTAO / 2, 550), (LARGURA/2 -LARGURA_BOTAO / 2, 550 + ALTURA_BOTAO), (LARGURA/2 + LARGURA_BOTAO / 2, 550 + ALTURA_BOTAO), (LARGURA/2 + LARGURA_BOTAO / 2, 550)]

# Função auxiliar para desenhar botões com texto centralizado
def desenhar_botao(pontos, texto, pos_mouse):

    x_min, y_min, x_max, y_max = pontos[0][0], pontos[0][1], pontos[2][0], pontos[2][1]

    x, y = pos_mouse

    # Verifica se o mouse está sobre o botão
    if x_min <= x <= x_max and y_min <= y <= y_max:
        cor_borda = VERDE_ESCURO
    else:
        cor_borda = VERDE_MUSGO

    # Desenha o fundo do botão e a borda
    desenhar_poligono(screen, pontos, cor_borda)

    # Renderiza e centraliza o texto dentro do botão
    superficie_texto = fonte_botao.render(texto, True, COR_TEXTO)
    screen.blit(superficie_texto, (x_min + (LARGURA_BOTAO - superficie_texto.get_width()) // 2, y_min + (ALTURA_BOTAO - superficie_texto.get_height()) // 2))

def verificar_click(pos_mouse, status):
    x, y = pos_mouse

    # Verifica se o mouse clicou em algum botão
    if btn_jogar[0][0] <= x <= btn_jogar[2][0] and btn_jogar[0][1] <= y <= btn_jogar[2][1]:
        return 2
    elif btn_ajuda[0][0] <= x <= btn_ajuda[2][0] and btn_ajuda[0][1] <= y <= btn_ajuda[2][1]:
        return 3
    elif btn_sair[0][0] <= x <= btn_sair[2][0] and btn_sair[0][1] <= y <= btn_sair[2][1]:
        return 4
    return status

def desenhar_menu(): 
    
    # Preenche o fundo do menu com uma cor sólida
    screen.fill((0, 0, 0))  # Preto

    # Renderiza o título do menu
    titulo = fonte_titulo.render("Webert Jonh", True, COR_TEXTO)
    screen.blit(titulo, ((LARGURA - titulo.get_width()) // 2, 150))

    # Obtém a posição atual do mouse
    pos_mouse = pygame.mouse.get_pos()

    # Desenha os botões com base na posição do mouse
    desenhar_botao(btn_jogar, "Jogar", pos_mouse)
    desenhar_botao(btn_ajuda, "Ajuda", pos_mouse)
    desenhar_botao(btn_sair, "Sair", pos_mouse)