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
LIMITE_QUEDA = ALTURA + 100
MAX_JUMP = 30
FORCA_MULT = 15

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


player = Sapo(INITIAL_X, INITIAL_Y)
player.pousar(plats[0])

carregando_pulo = False
jump_count = 0


rodando = True

while rodando:
    # ==========================
    # EVENTOS
    # ==========================
    for evento in pygame.event.get():

        # ==========================
        # QUIT GAME
        # ==========================
        if evento.type == pygame.QUIT:
            rodando = False

        # ======================================================================================================================
        # KEYDOWN
        #   Identifica spacebar pressionado -> Ativa booleano de controle de pulo 'carregando_pulo' se player não estiver no ar 
        # ======================================================================================================================
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            if not player.pulando:     
                carregando_pulo = True

        # =======================================================================================
        # KEYUP
        #   Identifica spacebar liberado -> 
        #       Desativa booleano de controle de pulo 'carregando_pulo'
        #       Calcula distância a ser cobrida no pulo e atribui na variável 'força'
        #       Chama método de movimento de player com parâmetro adequado 'player.pular(força)'
        #       Reseta variável de acumulador de pulo 'jump_count' para futuras movimentações
        # =======================================================================================
        
        elif evento.type == pygame.KEYUP and evento.key == pygame.K_SPACE:
            if carregando_pulo:
                carregando_pulo = False
                forca = jump_count * FORCA_MULT
                player.pular(forca)
                jump_count = 0

    
    # ============================================================================================================
    # RESET
    #   Identifica tecla 0 pressionada -> Reseta posição do player para a primeira plataforma, propósito de testes
    #   TODO: Mover método para dentro da classe Sapo
    # ============================================================================================================
    if pygame.key.get_pressed()[pygame.K_0]:
        player.x = INITIAL_X - Sapo.regulate_x
        player.y = INITIAL_Y - Sapo.regulate_y
        player.no_ar = False
        player.vel_y = 0


    # ==========================
    # DESENHOS
    # ==========================
    tela.fill(AZUL_AGUA) # Pinta tela inteira


    # Pecorrendo array de plataformas
    for plat in plats:
        if plat == plataforma_atual:
            plat.speed = 1.5
        plat.move_x_asis() # Movimento horizontal 
        plat.desenhar_plat(tela) # Desenho da plataforma


    # Exibição das margens 
    tela.blit(margem1.superficie, (margem1.x, margem1.y))
    tela.blit(margem2.superficie, (margem2.x, margem2.y))

    # ==========================
    # MOVIMENTAÇÃO
    # ==========================

    # -------------------------------------------------------------------------------------------------------------
    # JUMP_COUNT
    #   carregando_pulo: Booleano de controle, ativação por spacebar (Ver @Eventos)
    #   jump_count: Variável base responsável pelo movimento, escala com o tempo em que spacebar está pressionado
    #   MAX_JUMP: Constante que delimita o teto de jump_count, maior distância coberta em um único salto
    # -------------------------------------------------------------------------------------------------------------
    if carregando_pulo and jump_count <= MAX_JUMP:
        jump_count += 1

    plataforma_atual = player.check_underneath(plats)

    player.atualizar_pulo()

    if player.pulando:

        player.atualizar_pulo()

    else:

        if player.plataforma_atual is not None:
            
            player.move_alongside(player.plataforma_atual)

    if player.pulando:

        player.atualizar_pulo()

        plataforma = player.check_underneath(plats)

        if plataforma is not None:
            player.pousar(plataforma)
        else:       
            player.x, player.y = 720, 625
            player.no_ar = False
            player.vel_y = 0


    if player.y > LIMITE_QUEDA:
        player.x, player.y = INITIAL_X - 30, INITIAL_Y - 25
        player.no_ar = False
        player.vel_y = 0
        player.plataforma_atual = plats[0]

    player.desenhar_sap(tela)

    if carregando_pulo:
        texto = fonte.render("x", True, (255, 255, 255))
        tela.blit(texto, (player.x + 25, player.y - jump_count * 3))

    print(player.pulando)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()