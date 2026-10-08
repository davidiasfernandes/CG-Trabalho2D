# 🐸 Pula Webert!

Jogo arcade 2D desenvolvido como trabalho da disciplina de **Computação Gráfica (2026/1)**.
Todos os elementos visuais são renderizados com algoritmos gráficos implementados do zero — sem uso de funções de desenho de bibliotecas externas (apenas `pygame.Surface.set_at` como primitiva base).

## Descrição

**Pula Webert!** é um jogo de plataforma vertical no qual o jogador controla Webert Jonh, um sapo que precisa pular de vitória-régia em vitória-régia para atravessar um pântano perigoso. As plataformas se movem horizontalmente e o jogador deve dosar a força do pulo (segurando **ESPAÇO**) para pousar com segurança na próxima vitória-régia.

A resolução da janela é de **1500 × 750** pixels e o jogo roda a **60 FPS**.

---

## Como Jogar

### Controles

| Ação                  | Tecla                |
|-----------------------|----------------------|
| Carregar pulo         | Segurar `ESPAÇO`     |
| Soltar para pular     | Soltar `ESPAÇO`      |
| Cancelar pulo         | `X`                  |
| Resetar posição       | `0`                  |
| Voltar ao menu        | `Esc`                |
| Navegar menu          | Clique do mouse      |

### Objetivo

Pule de vitória-régia em vitória-régia até alcançar a margem final no topo do pântano. A barra de carregamento (gradiente verde → amarelo → vermelho) indica a força do pulo — domine o timing para não cair na água!

---

## Arquitetura do Código

```
CG-Trabalho2D/
├── main.py              # Loop principal, lógica do jogo, câmera e estados
├── Menu.py              # Tela de menu com botões interativos (mouse)
├── Sapo.py              # Classe do jogador (pulo, pouso, renderização, rotação)
├── Plataforma.py        # Classe das vitórias-régias (movimento, colisão)
├── Margem.py            # Margens laterais e margem final (meta)
├── Cores.py             # Paleta de cores do jogo
├── fimdejogo.py         # Tela de fim de jogo (fundo mapeado, elipses, linhas)
├── Requires/
│   └── Functions.py     # Biblioteca de algoritmos de Computação Gráfica
└── Assets/              # Sprites, fontes e músicas
    ├── sapo.png
    ├── sapo_menu.png
    ├── pedra.png
    ├── espinhos.png
    ├── fundo.png
    ├── Fonte-Pixel.ttf
    ├── trilha.mp3
    └── jogo_music.mp3
```

### Fluxo de Estados

```
Menu (1) ──► Jogo (2) ──► Fim de Jogo (5)
  │                            │
  ├──► Ajuda (3)               │
  ├──► Lore (6)                │
  ├──► Sair (4)                │
  │◄───────────────────────────┘  (Esc)
```

---

## Requisitos de Computação Gráfica

### a) Set Pixel

> **Arquivo:** `Requires/Functions.py` — função `setPixel()` (linha 4)

Toda a renderização do jogo passa por essa função. Ela escreve um pixel na superfície via `Surface.set_at()`, respeitando os limites da tela e a região de recorte ativa (`clip_atual`). É a primitiva base usada por todos os outros algoritmos.

```python
def setPixel(superficie, x, y, cor):
    x, y = int(x), int(y)
    if clip_atual:
        xmin, ymin, xmax, ymax = clip_atual
        if not (xmin <= x <= xmax and ymin <= y <= ymax):
            return
    if 0 <= x < superficie.get_width() and 0 <= y < superficie.get_height():
        superficie.set_at((x, y), cor)
```

---

### b) Primitivas de Rasterização (Linha, Círculo e Elipse)

> **Arquivo:** `Requires/Functions.py`

| Primitiva | Função | Uso no jogo |
|-----------|--------|-------------|
| **Linha (Bresenham)** | `bresenham()` (linha 18) | Arestas de polígonos (botões, barra de pulo, viewport) |
| **Linha (DDA)** | `dda()` (linha 154) | Linhas decorativas na tela de fim de jogo |
| **Círculo** | `desenhar_circulo()` (linha 58) | Vitórias-régias (plataformas) e sapo no minimapa |
| **Elipse** | `desenhar_elipse()` (linha 82) | Elementos decorativos (flores) na tela de fim de jogo |
| **Polígono** | `desenhar_poligono()` (linha 64) | Botões do menu, barra de carregamento, borda da viewport |

---

### c) Preenchimento de Regiões (Flood Fill / Boundary Fill e Scanline)

> **Arquivo:** `Requires/Functions.py`

| Algoritmo | Função | Uso no jogo |
|-----------|--------|-------------|
| **Flood Fill (iterativo)** | `flood_fill_iterativo()` (linha 229) | Preenchimento do fundo dos botões na tela de fim de jogo |
| **Scanline Fill** | `scanline_fill()` (linha 111) | Preenchimento das margens laterais e da margem final; preenchimento do minimapa |
| **Scanline Fill com Gradiente** | `scanline_fill_gradiente()` (linha 181) | Barra de carregamento do pulo (gradiente verde → amarelo → vermelho) |
| **Preenchimento de Região** | `preencher_regiao()` (linha 13) | Fundo da viewport (limpa o minimapa a cada frame) |

---

### d) Transformações Geométricas (Rotação, Translação e Escala)

> **Arquivo:** `Requires/Functions.py`

| Transformação | Função | Uso no jogo |
|---------------|--------|-------------|
| **Translação** | `translacao()` / `transladar_ponto()` (linhas 264, 310) | Movimento das plataformas, pulo do sapo, câmera |
| **Rotação** | `rotacao()` (linha 273) | Sapo do menu rotaciona em direção ao cursor do mouse |
| **Escala** | `escala()` / `escalar_pixels()` (linhas 88, 93) | Redimensionamento de sprites (sapo cresce durante o pulo), mapeamento de texturas |

Todas as transformações usam **coordenadas homogêneas** (matrizes 3×3) e a função `aplica_transformacao()` para multiplicar pontos pela matriz. A composição de transformações é feita por `multiplica_matrizes()`.

**Exemplo — Sapo crescendo durante o pulo** (`Sapo.py`, linha 118):
```python
self.fator = round((1 + (ESCALA_MAX - 1) * math.sin(math.pi * progresso)) * 20) / 20
```
O fator de escala segue uma curva senoidal para dar a sensação de profundidade.

---

### e) Animação 2D

| Animação | Arquivo | Descrição |
|----------|---------|-----------|
| **Pulo do sapo** | `Sapo.py` — `atualizar_pulo()` | O sapo se desloca verticalmente (translação) e escala suavemente (senoidal) durante o pulo |
| **Movimento das plataformas** | `Plataforma.py` — `move_x_asis()` | Plataformas transladam horizontalmente com inversão de direção nas margens |
| **Câmera** | `main.py` — `atualizar_camera()` | Scroll vertical suave acompanhando o progresso do jogador |
| **Barra de carregamento** | `main.py` — loop do jogo | Indicador oscila entre 0 e MAX_JUMP enquanto ESPAÇO está pressionado |
| **Sapo do menu** | `Menu.py` / `Sapo.py` — `desenhar_rotacionado()` | Sapo gigante que rotaciona em direção ao cursor do mouse |

---

### f) Janela e Viewport

> **Arquivo:** `Requires/Functions.py` — `janela_viewport()` (linha 335) e `desenhar_viewport()` (linha 390)

O jogo implementa a transformação **Janela → Viewport** com a cadeia clássica de matrizes:

1. **Translação** para a origem (−Wxmin, −Wymin)
2. **Escala** para ajustar proporções (sx, sy)
3. **Translação** para a viewport (+Vxmin, +Vymin)

Isso é usado para o **minimapa** no canto superior esquerdo, que projeta toda a área do jogo (1500 × ~2000 pixels) em uma janela miniatura (120 × N pixels). Dentro do minimapa são desenhados: as plataformas (círculos), a posição do sapo, o retângulo da câmera e a margem final.

---

### g) Recorte de Cohen-Sutherland (Clipping)

> **Arquivo:** `Requires/Functions.py` — `cohen_sutherland_clip()` (linha 418), `compute_code()` (linha 406) e integração em `bresenham()` (linha 18) e `dda()` (linha 154) | `Menu.py` — `desenhar_linhas_fundo()`

O recorte de linhas utiliza o **algoritmo de Cohen-Sutherland** para recortar segmentos de reta geometricamente contra a janela de recorte ativa (`clip_atual`) antes da etapa de rasterização. Cada extremidade da reta recebe um código binário de 4 bits (`INSIDE`, `LEFT`, `RIGHT`, `BOTTOM`, `TOP`) e o algoritmo calcula iterativamente os pontos de interseção com as bordas da janela delimitadora, descartando trechos externos ou aceitando o segmento recortado.

A integração é feita diretamente nas primitivas de rasterização de linha (`bresenham` e `dda`): quando uma região de recorte está ativa, a reta é recortada geometricamente antes de traçar qualquer pixel.

```python
# No início de bresenham() e dda():
if clip_atual:
    xmin, ymin, xmax, ymax = clip_atual
    aceito, x0, y0, x1, y1 = cohen_sutherland_clip(x0, y0, x1, y1, xmin, ymin, xmax, ymax)
    if not aceito:
        return  # linha totalmente fora — descarta
    x0, y0, x1, y1 = round(x0), round(y0), round(x1), round(y1)
```

#### Aplicações Práticas no Jogo:
1. **Fundo do Menu (`Menu.py`)**: Linhas diagonais suaves e estáticas são geradas com coordenadas que extrapolam amplamente os limites da tela (ex.: `y0 = -400`, `y1 = ALTURA + 400`, `x0 = -900`). O algoritmo de **Cohen-Sutherland calcula as interseções das retas com as 4 bordas da tela**, recortando geometricamente os segmentos externos antes da rasterização.
2. **Minimapa (`main.py` / `Requires/Functions.py`)**: A função `desenhar_viewport()` define `clip_atual = viewport` durante a execução de `conteudo_mini()`, garantindo que retas de polígonos (como o retângulo da câmera) não extravasem a miniatura.

---

### h) Mapeamento de Textura

> **Arquivos:** `Requires/Functions.py` — `escalar_pixels()` (linha 93) | `Sapo.py` | `fimdejogo.py`

O mapeamento de textura é feito pela **transformação inversa**: para cada pixel do destino, calcula-se o pixel correspondente na imagem original usando a matriz inversa de escala. Isso permite redimensionar sprites arbitrariamente sem distorção.

| Uso | Arquivo | Descrição |
|-----|---------|-----------|
| **Sprite do sapo** | `Sapo.py` — `obter_pixels()` / `desenhar_sap()` | Sapo é mapeado em diferentes tamanhos conforme o fator de escala do pulo |
| **Sapo rotacionado do menu** | `Sapo.py` — `obter_rotacionado()` | Aplica rotação inversa para mapear cada pixel do destino à textura original |
| **Fundo da tela final** | `fimdejogo.py` — `criar_fundo_pixels()` | Imagem `fundo.png` é mapeada pixel a pixel na tela usando `escalar_pixels()` |

O sistema usa **cache** para evitar recalcular o mapeamento a cada frame.

---

### i) Input (Teclado e Mouse)

| Tipo | Arquivo | Uso |
|------|---------|-----|
| **Teclado — ESPAÇO** | `main.py` — `jogo()` | Segurar para carregar pulo, soltar para pular |
| **Teclado — X** | `main.py` — `jogo()` | Cancelar pulo carregado |
| **Teclado — 0** | `main.py` — `jogo()` | Resetar posição do sapo |
| **Teclado — Esc** | `main.py` — loop principal | Voltar ao menu de qualquer tela |
| **Mouse — Clique** | `main.py` / `Menu.py` — `verificar_click()` | Navegação nos botões do menu |
| **Mouse — Posição** | `Menu.py` — `desenhar_menu()` | Hover nos botões (muda cor) e rotação do sapo na direção do cursor |

---

## Como Executar

### Pré-requisitos

- **Python** 3.10+
- **Pygame**

### Instalação

```bash
# Clone o repositório
git clone https://github.com/davidiasfernandes/CG-Trabalho2D.git
cd CG-Trabalho2D

# Instale as dependências
pip install pygame

# Execute o jogo
python main.py
```