import pygame
from Menu import desenhar_menu, verificar_click
from Requires import Functions
from Requires.Functions import aplica_transformacao, desenhar_circulo, desenhar_poligono, janela_viewport, preencher_regiao
from Requires.Functions import scanline_fill_gradiente, desenhar_viewport, transladar_ponto
from Plataforma import RAIO, Plataforma, SPEED
from Margem import LARGURA_MARGEM, Margem, MargemFinal, ALTURA_FINAL
from Sapo import Sapo
from Cores import AZUL_AGUA, BRANCO, VERDE_ESCURO, MARGEM
from fimdejogo import desenhar_tela_final

pygame.mixer.music.load("./Assets/trilha.mp3")
pygame.mixer.music.set_volume(0.65)
pygame.mixer.music.play(-1)

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
TEMPO_CARGA = 0.85  # segundos segurando para ir de zero até a força máxima
PASSO_CARGA = MAX_JUMP / (TEMPO_CARGA * 60)  # quanto a carga muda por frame (60 FPS)
FORCA_MULT = 14
ALTURA_CARREGAMENTO = 100

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Gagalin", 18)

global status
status = 1  # 1 = menu, 2 = jogo, 3 = ajuda, 4 = sair
plats = calculate_plats(INITIAL_X, INITIAL_Y, 6, 275)

# Margem final: fica onde antes ficava a última plataforma
y_centro_final = INITIAL_Y - 6 * 275
margem_final = MargemFinal(0, y_centro_final - ALTURA_FINAL // 2)
margem_final.draw()

janela = (0, margem_final.y, LARGURA, ALTURA)
MINI_L = 120
MINI_A = round(MINI_L * (janela[3] - janela[1]) / (janela[2] - janela[0]))
viewport = (10, 50, 10 + MINI_L, 50 + MINI_A)
M_MINI = janela_viewport(janela, viewport)

def conteudo_mini():
    r = Plataforma.raio * M_MINI[0][0]
    for p in plats:
        (cx, cy), = aplica_transformacao(M_MINI, [(p.x, p.y)])
        desenhar_circulo(tela, cx, cy, r, (120, 255, 80))
    (sx, sy), = aplica_transformacao(M_MINI, [player.get_centro()])
    desenhar_circulo(tela, sx, sy, 3, BRANCO)
    cam = [(0, camera_y), (LARGURA, camera_y), (LARGURA, camera_y + ALTURA), (0, camera_y + ALTURA)]
    desenhar_poligono(tela, aplica_transformacao(M_MINI, cam), BRANCO)
    desenhar_poligono(tela, aplica_transformacao(M_MINI, [(0, margem_final.y), (LARGURA, margem_final.y), (LARGURA, margem_final.y + ALTURA_FINAL), (0, margem_final.y + ALTURA_FINAL)]), MARGEM)
    Functions.scanline_fill(tela, aplica_transformacao(M_MINI, [(0, margem_final.y), (LARGURA, margem_final.y), (LARGURA, margem_final.y + ALTURA_FINAL), (0, margem_final.y + ALTURA_FINAL)]), MARGEM)

plats[0].speed = 0

margem1 = Margem(0, 0)
margem2 = Margem(LARGURA - LARGURA_MARGEM, 0)
margem1.draw()
margem2.draw()

player = Sapo(INITIAL_X, INITIAL_Y)
player.pousar(plats[0])
plataforma_atual = plats[0]

pontos = 0
chegou = False
carregando_pulo = False
jump_count = 0
carga_dir = 1  # 1 = subindo, -1 = descendo
afundando = False
fonte_ajuda = pygame.font.Font("./Assets/Fonte-Pixel.ttf", 24)
fonte_ajuda2 = pygame.font.Font("./Assets/Fonte-Pixel.ttf", 16)

def atualizar_camera():
    global camera_y

    if camera_y < camera_alvo:
        dy = VELOCIDADE_CAMERA
        if camera_y + dy > camera_alvo:
            dy = camera_alvo - camera_y
        _, camera_y = transladar_ponto(0, camera_y, 0, dy)

    elif camera_y > camera_alvo:
        dy = -VELOCIDADE_CAMERA_RETORNO
        if camera_y + dy < camera_alvo:
            dy = camera_alvo - camera_y
        _, camera_y = transladar_ponto(0, camera_y, 0, dy)

def verificar_camera(plat):

    global camera_alvo

    indice = plats.index(plat)

    # A cada plataforma ímpar:
    # P3 -> revela P4 e P5
    # P5 -> revela P6 e a margem final

    if indice >= 2 and indice % 2 == 0:

        if indice + 2 >= len(plats):
            camera_alvo = margem_final.y
        else:
            camera_alvo = plats[indice + 2].y - 100

def resetar_sapo():

    global plataforma_atual
    global carregando_pulo
    global jump_count
    global afundando
    global camera_alvo
    global pontos
    global chegou

    player.pousar(plats[0])

    plataforma_atual = plats[0]

    carregando_pulo = False
    jump_count = 0

    afundando = False
    pontos = 0
    chegou = False
    camera_alvo = 0

def jogo(eventos):
    global carregando_pulo, jump_count, carga_dir, afundando, plataforma_atual, pontos, status, chegou

    for evento in eventos:
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            if not player.pulando and not afundando:
                carregando_pulo = True
                jump_count = 0
                carga_dir = 1
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_x:
            if carregando_pulo:
                carregando_pulo = False
                jump_count = 0
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
        # Quando o pulo termina, chega na margem final, pousa se houver plataforma embaixo, senão afunda
        if not player.pulando:
            if player.get_centro()[1] <= margem_final.y + ALTURA_FINAL:
                chegou = True
            else:
                # Pousa se o centro do sapo estiver dentro do círculo de alguma plataforma
                plat = player.check_underneath(plats)
                if plat is not None:
                    player.pousar(plat)
                    plataforma_atual = plat
                    verificar_camera(plat)
                    pontos = max(pontos, plats.index(plat))
                else:
                    player.plataforma_atual = None
                    afundando = True

    # Afunda e volta para a plataforma inicial
    if afundando:
        resetar_sapo()

    # Sapo parado acompanha o movimento da plataforma
    if not player.pulando and not afundando:
        if player.plataforma_atual is not None and player.plataforma_atual.speed > 0:
            player.move_alongside(player.plataforma_atual)

    atualizar_camera()

    status = 5 if chegou else 2

    tela.fill(AZUL_AGUA)

    ##### Renderização: plataformas, margens, sapo e carregamento do pulo (barra vertical com gradiente de vermelho para verde)
    if not carregando_pulo and not player.pulando and not afundando:
        aviso = fonte.render("Pressione 'ESPAÇO' para carregar o pulo", True, (255, 255, 255))
        tela.blit(aviso, ((LARGURA - aviso.get_width()) // 2, ALTURA - 30))

    if carregando_pulo:
        player_tela_y = player.y - camera_y
        poligono = [(player.x + 30, player_tela_y + 2), (player.x + 30, player_tela_y - ALTURA_CARREGAMENTO/2), (player.x + 30, player_tela_y + 10 - ALTURA_CARREGAMENTO), (player.x + 55, player_tela_y + 10 - ALTURA_CARREGAMENTO), (player.x + 55, player_tela_y - ALTURA_CARREGAMENTO/2), (player.x + 55, player_tela_y + 2)]
        scanline_fill_gradiente(tela, poligono, [(0, 255, 0), (255, 255, 0), (255, 0, 0), (255, 0, 0), (255, 255, 0), (0, 255, 0)])
        desenhar_poligono(tela, poligono, VERDE_ESCURO)
        texto = fonte.render("    ------", True, (0, 0, 0))
        tela.blit(texto, (player.x + 19, player_tela_y - 5 - jump_count * 3))  

    for plat in plats:
        tela_y = plat.y - camera_y
        # Só desenha se estiver próximo da área visível.
        if -RAIO <= tela_y <= ALTURA + RAIO:
            plat.desenhar_plat(tela, camera_y)

    tela.blit(margem_final.superficie, (margem_final.x, margem_final.y - camera_y))
    tela.blit(margem1.superficie, (margem1.x, margem1.y))
    tela.blit(margem2.superficie, (margem2.x, margem2.y))
    player.desenhar_sap(tela, camera_y)

    texto_pontos = fonte.render(f"Escore: {pontos}", True, (255, 255, 255))
    tela.blit(texto_pontos, (20, 20))

    desenhar_viewport(tela, viewport, BRANCO, conteudo_mini)

rodando = True
while rodando:
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and status == 1:
            status = verificar_click(pygame.mouse.get_pos(), status)
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE and status in (2, 3, 5, 6):
            status = 1

    if status == 1:
        desenhar_menu()
    elif status == 2:
        jogo(eventos)
    elif status == 3:
        tela.fill((0, 0, 0))
        ajuda_titulo = fonte_ajuda.render("Ajuda: \n\n\n", True, (0, 255, 0))
        tela.blit(ajuda_titulo, ((LARGURA - ajuda_titulo.get_width()) // 2, ALTURA // 8))
        ajuda = fonte_ajuda.render("Pressione e segure 'ESPAÇO' para carregar o pulo. \n\nCuidado! É mais perigoso do que parece... \n\nA barra preta indica a força de seu pulo, estude para aumentar sua chance de pousar na vitória régia da frente! \n\nPara cancelar o pulo, pressione 'X'.\n\n", True, (255, 255, 255))
        tela.blit(ajuda, ((LARGURA - ajuda.get_width()) // 2, ALTURA // 4))
        ajuda2 = fonte_ajuda2.render("\nClique \"Esc\" para voltar ao menu.", True, (0, 100, 255))
        tela.blit(ajuda2, ((LARGURA - ajuda2.get_width()) // 2, ALTURA // 4 + 300))
    elif status == 4:
        rodando = False
    elif status == 5:
        resetar_sapo()
        pontos = 0
        desenhar_tela_final()
    elif status == 6:
        tela.fill((0, 0, 0))
        lore_titulo = fonte_ajuda.render("Lore: \n\n\n", True, (255, 0, 0))
        tela.blit(lore_titulo, ((LARGURA - lore_titulo.get_width()) // 2, ALTURA // 8))
        lore = fonte_ajuda.render("Webert Jonh é um sapo que vive em um pântano cheio de perigos. \n\nEle precisa pular de vitória-régia em vitória-régia para atravessar o pântano e chegar ao outro lado. \n\nMas cuidado! Nem todas as vitórias-régias são seguras, algumas podem afundar ou estar muito distantes. \n\nUse sua habilidade e estratégia para ajudar Webert a atravessar o pântano com segurança!\n\n", True, (255, 255, 255))
        tela.blit(lore, ((LARGURA - lore.get_width()) // 2, ALTURA // 4))
        lore2 = fonte_ajuda2.render("\nClique \"Esc\" para voltar ao menu.", True, (0, 100, 255))
        tela.blit(lore2, ((LARGURA - lore2.get_width()) // 2, ALTURA // 4 + 300))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()