import math

from Cores import AZUL_AGUA, BRANCO, VERDE_ESCURO
def setPixel(superficie, x, y, cor):
    x, y = int(x), int(y)
    if clip_atual:
        xmin, ymin, xmax, ymax = clip_atual
        if not (xmin <= x <= xmax and ymin <= y <= ymax):
            return
    if 0 <= x < superficie.get_width() and 0 <= y < superficie.get_height():
        superficie.set_at((x, y), cor)

def preencher_regiao(superficie, xmin, ymin, xmax, ymax, cor):
    for y in range(int(ymin), int(ymax) + 1):
        for x in range(int(xmin), int(xmax) + 1):
            setPixel(superficie, x, y, cor)

def bresenham(superficie, x0, y0, x1, y1, cor):
    if clip_atual:
        xmin, ymin, xmax, ymax = clip_atual
        aceito, x0, y0, x1, y1 = cohen_sutherland_clip(x0, y0, x1, y1, xmin, ymin, xmax, ymax)
        if not aceito:
            return
        x0, y0, x1, y1 = round(x0), round(y0), round(x1), round(y1)

    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    ystep = 1 if dy >= 0 else -1
    dy = abs(dy)

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    y = y0
    for x in range(int(x0), int(x1 + 1)):
        if steep:
            setPixel(superficie, y, x, cor)
        else:
            setPixel(superficie, x, y, cor)

        if d > 0:
            y += ystep
            d += incNE
        else:
            d += incE
            
def desenhar_circulo(superficie, x, y, raio, cor):
    for px in range(int(x - raio), int(x + raio + 1)):
        for py in range(int(y - raio), int(y + raio + 1)):
            if (px - x) ** 2 + (py - y) ** 2 <= raio ** 2:
                setPixel(superficie, px, py, cor)

def desenhar_poligono(superficie, pontos, cor_borda):
    n = len(pontos)
    for i in range(n):
        x0, y0 = pontos[i]
        x1, y1 = pontos[(i + 1) % n]
        bresenham(superficie, x0, y0, x1, y1, cor_borda)

def interpola_cor(c1, c2, t):
    r = int(c1[0] + (c2[0]-c1[0])*t)
    g = int(c1[1] + (c2[1]-c1[1])*t)
    b = int(c1[2] + (c2[2]-c1[2])*t)

    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    
    return (r, g, b)

def desenhar_elipse(superficie, x, y, rx, ry, cor):
    for px in range(int(x - rx), int(x + rx + 1)):
        for py in range(int(y - ry), int(y + ry + 1)):
            if ((px - x) / rx) ** 2 + ((py - y) / ry) ** 2 <= 1:
                setPixel(superficie, px, py, cor)

def escala(sx, sy):
    return [[sx, 0, 0], 
            [0, sy, 0], 
            [0,  0, 1]]

def escalar_pixels(imagem, nova_larg, nova_alt):
    larg, alt = imagem.get_size()
    m = escala(larg / nova_larg, alt / nova_alt)  # inversa da escala: destino -> origem
    pixels = []
    for xd in range(nova_larg):
        for yd in range(nova_alt):
            xo = m[0][0] * xd + m[0][1] * yd + m[0][2]
            yo = m[1][0] * xd + m[1][1] * yd + m[1][2]
            cor = imagem.get_at((int(xo), int(yo)))
            if cor.a > 128:
                pixels.append((xd, yd, tuple(cor)))
    return pixels

def obter_pixels(self, larg, alt):
            if (larg, alt) not in self.cache:
                self.cache[(larg, alt)] = escalar_pixels(self.imagem, larg, alt)
            return self.cache[(larg, alt)]

def scanline_fill(superficie, pontos, cor_preenchimento):
    # Encontra Y mínimo e máximo
    ys = [p[1] for p in pontos]
    y_min = int(min(ys))
    y_max = int(max(ys))

    n = len(pontos)

    for y in range(y_min, y_max):
        intersecoes_x = []

        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]

            # Ignora arestas horizontais
            if y0 == y1:
                continue

            # Garante y0 < y1
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0

            # Regra Ymin ≤ y < Ymax
            if y < y0 or y >= y1:
                continue

            # Calcula interseção
            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            intersecoes_x.append(x)

        # Ordena interseções
        intersecoes_x.sort()

        # Preenche entre pares
        for i in range(0, len(intersecoes_x), 2):
            if i + 1 < len(intersecoes_x):
                x_inicio = int(round(intersecoes_x[i]))
                x_fim = int(round(intersecoes_x[i + 1]))

                for x in range(x_inicio, x_fim + 1):
                    setPixel(superficie, x, y, cor_preenchimento)

def dda(superficie, x0, y0, x1, y1, cor):
    if clip_atual:
        xmin, ymin, xmax, ymax = clip_atual
        aceito, x0, y0, x1, y1 = cohen_sutherland_clip(x0, y0, x1, y1, xmin, ymin, xmax, ymax)
        if not aceito:
            return

    dx = x1 - x0
    dy = y1 - y0

    passos = max(abs(dx), abs(dy))

    if passos == 0:
        setPixel(superficie, x0, y0, cor)
        return

    x_inc = dx / passos
    y_inc = dy / passos

    x = x0
    y = y0

    for _ in range(passos + 1):
        setPixel(superficie, round(x), round(y), cor)
        x += x_inc
        y += y_inc
    
def scanline_fill_gradiente(superficie, pontos, cores):
    ys = [p[1] for p in pontos]
    y_min = int(min(ys))
    y_max = int(max(ys))

    n = len(pontos)

    for y in range(y_min, y_max):
        intersecoes = []

        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]

            c0 = cores[i]
            c1 = cores[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                c0, c1 = c1, c0

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)
            x = x0 + t * (x1 - x0)
            cor_y = interpola_cor(c0, c1, t)

            intersecoes.append((x, cor_y))

        intersecoes.sort(key=lambda i: i[0])

        for i in range(0, len(intersecoes), 2):
            if i + 1 < len(intersecoes):
                x_ini, cor_ini = intersecoes[i]
                x_fim, cor_fim = intersecoes[i + 1]

                if x_fim == x_ini:
                    continue

                for x in range(int(x_ini), int(x_fim) + 1):
                    t = (x - x_ini) / (x_fim - x_ini)
                    cor = interpola_cor(cor_ini, cor_fim, t)
                    setPixel(superficie, x, y, cor)

def flood_fill_iterativo(superficie, x, y, cor_preenchimento, cor_borda):
    largura = superficie.get_width()
    altura = superficie.get_height()

    pilha = [(x, y)]

    while pilha:
        x, y = pilha.pop()

        if not (0 <= x < largura and 0 <= y < altura):
            continue

        cor_atual = superficie.get_at((x, y))[:3]

        if cor_atual == cor_borda or cor_atual == cor_preenchimento:
            continue

        setPixel(superficie, x, y, cor_preenchimento)

        pilha.append((x + 1, y))
        pilha.append((x - 1, y))
        pilha.append((x, y + 1))
        pilha.append((x, y - 1))

clip_atual = None

def identidade():

    return [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]


def translacao(tx, ty):

    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]


def rotacao(theta):

    c = math.cos(theta)
    s = math.sin(theta)

    return [
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ]

def aplica_transformacao(m, pontos):

    novos = []

    for x, y in pontos:

        v = [x, y, 1]

        x_novo = (
            m[0][0] * v[0]
            + m[0][1] * v[1]
            + m[0][2]
        )

        y_novo = (
            m[1][0] * v[0]
            + m[1][1] * v[1]
            + m[1][2]
        )

        novos.append(
            (x_novo, y_novo)
        )

    return novos

def transladar_ponto(x, y, dx, dy):
    T = translacao(dx, dy)
    (novo_x, novo_y), = aplica_transformacao(T, [(x, y)])
    return novo_x, novo_y

def multiplica_matrizes(a, b):

    r = [
        [0] * 3
        for _ in range(3)
    ]

    for i in range(3):
        for j in range(3):
            for k in range(3):

                r[i][j] += (
                    a[i][k]
                    * b[k][j]
                )

    return r



def janela_viewport(janela, viewport):

    Wxmin, Wymin, Wxmax, Wymax = janela
    Vxmin, Vymin, Vxmax, Vymax = viewport

    sx = (
        (Vxmax - Vxmin)
        / (Wxmax - Wxmin)
    )

    sy = (
        (Vymax - Vymin)
        / (Wymax - Wymin)
    )

    # ------------------------------------------------
    # 1. Janela -> origem
    # -------------------------------------------------

    M = identidade()

    M = multiplica_matrizes(
        translacao(
            -Wxmin,
            -Wymin
        ),
        M
    )

    # -------------------------------------------------
    # 2. Escala
    # -------------------------------------------------

    M = multiplica_matrizes(
        escala(
            sx,
            sy
        ),
        M
    )

    # -------------------------------------------------
    # 3. Origem -> viewport
    # -------------------------------------------------

    M = multiplica_matrizes(
        translacao(
            Vxmin,
            Vymin
        ),
        M
    )

    return M

def desenhar_viewport(superficie, viewport, cor_borda, conteudo=None):
    global clip_atual
    Vxmin, Vymin, Vxmax, Vymax = viewport
    clip_atual = viewport
    preencher_regiao(superficie, Vxmin, Vymin, Vxmax, Vymax, AZUL_AGUA)
    if conteudo:
        conteudo()
    clip_atual = None
    desenhar_poligono(superficie, [(Vxmin, Vymin), (Vxmax, Vymin), (Vxmax, Vymax), (Vxmin, Vymax)], cor_borda)

INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

def compute_code(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    code1 = compute_code(x1, y1, xmin, ymin, xmax, ymax)
    code2 = compute_code(x2, y2, xmin, ymin, xmax, ymax)
    accept = False

    while True:
        if code1 == 0 and code2 == 0:
            accept = True
            break
        elif (code1 & code2) != 0:
            break
        else:
            x, y = 0, 0
            code_out = code1 if code1 != 0 else code2
            if code_out & TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2, xmin, ymin, xmax, ymax)

    return accept, x1, y1, x2, y2
