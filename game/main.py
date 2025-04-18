import pygame
from pyamaze import maze

# --- Configurações do jogo ---
TAM_CELULA = 40
FPS = 60
COR_PAREDE = (0, 0, 0)
COR_CAMINHO = (255, 255, 255)
COR_JOGADOR = (50, 100, 255)
COR_OBJETIVO = (0, 200, 0)
COR_TEXTO = (0, 0, 0)

# Gerar o labirinto
m = maze(10, 10)
m.CreateMaze()
mapa = m.maze_map

# Inicializar pygame
pygame.init()
largura_tela = m.cols * TAM_CELULA
altura_tela = m.rows * TAM_CELULA + 50
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Labirinto - Chegue ao objetivo")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 30)
fonte_vitoria = pygame.font.SysFont(None, 40)

# Posição inicial e contador
pos_linha = m.rows
pos_coluna = m.cols
passos = 0
venceu = False

def desenhar_labirinto():
    for linha in range(1, m.rows+1):
        for coluna in range(1, m.cols+1):
            celula = mapa[(linha, coluna)]
            x = (coluna - 1) * TAM_CELULA
            y = (linha - 1) * TAM_CELULA

            pygame.draw.rect(tela, COR_CAMINHO, (x, y, TAM_CELULA, TAM_CELULA))

            if celula['N'] == 0:
                pygame.draw.line(tela, COR_PAREDE, (x, y), (x + TAM_CELULA, y), 3)
            if celula['S'] == 0:
                pygame.draw.line(tela, COR_PAREDE, (x, y + TAM_CELULA), (x + TAM_CELULA, y + TAM_CELULA), 3)
            if celula['W'] == 0:
                pygame.draw.line(tela, COR_PAREDE, (x, y), (x, y + TAM_CELULA), 3)
            if celula['E'] == 0:
                pygame.draw.line(tela, COR_PAREDE, (x + TAM_CELULA, y), (x + TAM_CELULA, y + TAM_CELULA), 3)

    # Desenhar objetivo (canto superior esquerdo)
    obj_x = 0 + TAM_CELULA // 4
    obj_y = 0 + TAM_CELULA // 4
    pygame.draw.rect(tela, COR_OBJETIVO, (obj_x, obj_y, TAM_CELULA // 2, TAM_CELULA // 2))

def desenhar_passos():
    texto = fonte.render(f"Passos: {passos}", True, COR_TEXTO)
    tela.blit(texto, (10, m.rows * TAM_CELULA + 10))

def mostrar_mensagem_vitoria():
    mensagem = fonte_vitoria.render(f"🎉 Você venceu em {passos} passos!", True, (0, 150, 0))
    tela.blit(mensagem, (largura_tela // 2 - mensagem.get_width() // 2, altura_tela - 40))

# Loop principal
rodando = True
while rodando:
    tela.fill(COR_PAREDE)
    desenhar_labirinto()
    desenhar_passos()

    # Jogador
    jogador_x = (pos_coluna - 1) * TAM_CELULA + TAM_CELULA // 4
    jogador_y = (pos_linha - 1) * TAM_CELULA + TAM_CELULA // 4
    pygame.draw.rect(tela, COR_JOGADOR, (jogador_x, jogador_y, TAM_CELULA // 2, TAM_CELULA // 2))

    if venceu:
        mostrar_mensagem_vitoria()

    pygame.display.flip()
    relogio.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN and not venceu:
            celula_atual = mapa[(pos_linha, pos_coluna)]

            if evento.key == pygame.K_UP and celula_atual['N'] == 1:
                pos_linha -= 1
                passos += 1
            elif evento.key == pygame.K_DOWN and celula_atual['S'] == 1:
                pos_linha += 1
                passos += 1
            elif evento.key == pygame.K_LEFT and celula_atual['W'] == 1:
                pos_coluna -= 1
                passos += 1
            elif evento.key == pygame.K_RIGHT and celula_atual['E'] == 1:
                pos_coluna += 1
                passos += 1

            # Verificar vitória
            if pos_linha == 1 and pos_coluna == 1:
                venceu = True

pygame.quit()
