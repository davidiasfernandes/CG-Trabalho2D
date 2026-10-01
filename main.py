import pygame
from Menu import desenhar_menu, verificar_click
from Requires.Functions import desenhar_poligono
from Requires.Functions import scanline_fill_gradiente
from Plataforma import RAIO, Plataforma, SPEED
from Margem import Margem
from Sapo import Sapo
from Cores import AZUL_AGUA, VERDE_ESCURO


def calculate_plats(initial_lenght, initial_height, quantidade, space_between):

    return [
        Plataforma(
            initial_lenght,
            initial_height - i * space_between
        )
        for i in range(quantidade)
    ]


# Configurações
LARGURA, ALTURA = 1500, 750
# Câmera
camera_y = 0
camera_alvo = 0
VELOCIDADE_CAMERA = 12
VELOCIDADE_CAMERA_RETORNO = 25

INITIAL_X, INITIAL_Y = 750, 650
MAX_JUMP = 30
TEMPO_CARGA = 1  # segundos segurando para ir de zero até a força máxima
PASSO_CARGA = MAX_JUMP / (TEMPO_CARGA * 60)  # quanto a carga muda por frame (60 FPS)
FORCA_MULT = 14
VELOCIDADE_AFOGAMENTO = 8
ALTURA_CARREGAMENTO = 100

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Gagalin", 18)

status = 1  # 1 = menu, 2 = jogo, 3 = ajuda, 4 = sair
plats = calculate_plats(INITIAL_X, INITIAL_Y, 10, 275)
plats[0].speed = 0

margem1 = Margem(0, 0)
margem2 = Margem(LARGURA - 200, 0)
margem1.draw()
margem2.draw()

player = Sapo(INITIAL_X, INITIAL_Y)
player.pousar(plats[0])
plataforma_atual = plats[0]

carregando_pulo = False
jump_count = 0
carga_dir = 1  # 1 = carga subindo, -1 = descendo
afundando = False
alpha_sapo = 255
fonte_ajuda = pygame.font.Font("./Assets/Fonte-Pixel.ttf", 24)

def atualizar_camera():

    global camera_y

    if camera_y < camera_alvo:

        camera_y += VELOCIDADE_CAMERA

        if camera_y > camera_alvo:
            camera_y = camera_alvo

    elif camera_y > camera_alvo:

        camera_y -= VELOCIDADE_CAMERA_RETORNO

        if camera_y < camera_alvo:
            camera_y = camera_alvo

def verificar_camera(plat):

    global camera_alvo

    indice = plats.index(plat)

    # A cada plataforma ímpar:
    # P3 -> revela P4 e P5
    # P5 -> revela P6 e P7

    if indice >= 2 and indice % 2 == 0:

        proxima_ultima = min(indice + 2, len(plats) - 1)

        # Queremos que a nova última plataforma
        # fique na mesma região superior da tela.
        camera_alvo = plats[proxima_ultima].y - 100

def resetar_sapo():

    global plataforma_atual
    global carregando_pulo
    global jump_count
    global afundando
    global alpha_sapo
    global camera_alvo

    player.pousar(plats[0])

    plataforma_atual = plats[0]

    carregando_pulo = False
    jump_count = 0

    afundando = False
    alpha_sapo = 255

    camera_alvo = 0

def jogo(eventos):
    global carregando_pulo, jump_count, carga_dir, afundando, alpha_sapo, plataforma_atual
    for evento in eventos:
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            if not player.pulando and not afundando:
                carregando_pulo = True
                jump_count = 0
                carga_dir = 1
        elif evento.type == pygame.KEYUP and evento.key == pygame.K_SPACE:
            if carregando_pulo:
                carregando_pulo = False
                player.pular(jump_count * FORCA_MULT)
                jump_count = 0

    if pygame.key.get_pressed()[pygame.K_0]:
        resetar_sapo()

    # A carga sobe até o máximo e desce até zero, repetindo enquanto o espaço estiver pressionado
    if carregando_pulo:
        jump_count += PASSO_CARGA * carga_dir
        if jump_count >= MAX_JUMP:
            jump_count = MAX_JUMP
            carga_dir = -1
        elif jump_count <= 0:
            jump_count = 0
            carga_dir = 1

    # Movimento das plataformas: a inicial fica parada e a que tem o sapo anda mais devagar
    for plat in plats:
        if plat == plats[0]:
            plat.speed = 0
        elif plat == plataforma_atual:
            plat.speed = 1.5
        else:
            plat.speed = SPEED
        if plat.speed > 0:
            plat.move_x_asis()

    if player.pulando:
        player.atualizar_pulo()
        # Quando o pulo termina, pousa se houver plataforma embaixo; senão afunda no lugar
        if not player.pulando:
            # Pousa se o centro do sapo estiver dentro do círculo de alguma plataforma
            plat = player.check_underneath(plats)
            if plat is not None:
                player.pousar(plat)
                plataforma_atual = plat
                verificar_camera(plat)
            else:
                player.plataforma_atual = None
                afundando = True
                alpha_sapo = 255

    # Afunda ficando transparente; ao sumir, volta para a plataforma inicial
    if afundando:
        alpha_sapo -= VELOCIDADE_AFOGAMENTO
        if alpha_sapo <= 0:
            resetar_sapo()

    # Sapo parado acompanha o movimento da plataforma
    if not player.pulando and not afundando:
        if player.plataforma_atual is not None and player.plataforma_atual.speed > 0:
            player.move_alongside(player.plataforma_atual)

    atualizar_camera()

    tela.fill(AZUL_AGUA)

    # Renderização: plataformas, margens, sapo e carregamento do pulo (barra vertical com gradiente de vermelho para verde)
    if carregando_pulo:
        player_tela_y = player.y - camera_y
        poligono = [(player.x + 30, player_tela_y + 2), (player.x + 30, player_tela_y - ALTURA_CARREGAMENTO/2), (player.x + 30, player_tela_y + 10 - ALTURA_CARREGAMENTO), (player.x + 55, player_tela_y + 10 - ALTURA_CARREGAMENTO), (player.x + 55, player_tela_y - ALTURA_CARREGAMENTO/2), (player.x + 55, player_tela_y + 2)]
        scanline_fill_gradiente(tela, poligono, [(255, 0, 0), (0, 255, 0), (255, 0, 0), (255, 0, 0), (0, 255, 0), (255, 0, 0)])
        desenhar_poligono(tela, poligono, VERDE_ESCURO)

    for plat in plats:
        tela_y = plat.y - camera_y
        # Só desenha se estiver próximo da área visível.
        if -RAIO <= tela_y <= ALTURA + RAIO:
            plat.desenhar_plat(tela, camera_y)

    tela.blit(margem1.superficie, (margem1.x, margem1.y))
    tela.blit(margem2.superficie, (margem2.x, margem2.y))
    player.desenhar_sap(tela, alpha_sapo, camera_y)

    if carregando_pulo:
        texto = fonte.render("    ------", True, (255, 255, 255))
        tela.blit(texto, (player.x + 19, player_tela_y - 5 - jump_count * 3))

rodando = True
while rodando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and status == 1:
            status = verificar_click(pygame.mouse.get_pos(), status)
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE and status in (2, 3):
            status = 1

    if status == 1:
        desenhar_menu()
    elif status == 2:
        jogo(eventos)
    elif status == 3:
        tela.fill((0, 0, 0))
        ajuda = fonte_ajuda.render("Pressione ESPAÇO para carregar o pulo \n\nCuidado com o pulo, ele pode ser mais perigoso do que parece \n\nO mais próximo que chegar ao verde, maior sua chance de pousar na vitória régia da frente!", True, (255, 255, 255))
        tela.blit(ajuda, ((LARGURA - ajuda.get_width()) // 2, ALTURA // 4))
    elif status == 4:
        rodando = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
