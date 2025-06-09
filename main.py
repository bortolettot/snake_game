import pygame
import time
import random

# Inicializar o pygame
pygame.init()

# Definir as cores
branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (213, 50, 80)
verde = (0, 255, 0)
azul = (50, 153, 213)
cinza = (100, 100, 100)

# Configurações da tela
largura = 800
altura = 600

display = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da Cobra')

clock = pygame.time.Clock()

# Tamanho do bloco da cobra
bloco_cobra = 10

# Parametros que variam conforme a dificuldade
velocidade = 15
TEMPO_PAUSA = 5
NUM_OBSTACULOS = 5

# Fonte do texto
fonte = pygame.font.SysFont("bahnschrift", 25)
fonte_pontuacao = pygame.font.SysFont("comicsansms", 35)

def pontuacao(pontos_jogador, pontos_bot):
    texto = f"Voce: {pontos_jogador}  Bot: {pontos_bot}"
    valor = fonte_pontuacao.render(texto, True, azul)
    display.blit(valor, [0, 0])

def desenha_cobra(cor, bloco_cobra, lista_cobra):
    for x in lista_cobra:
        pygame.draw.rect(display, cor, [x[0], x[1], bloco_cobra, bloco_cobra])

def desenha_obstaculos(obstaculos):
    for o in obstaculos:
        pygame.draw.rect(display, cinza, [o[0], o[1], bloco_cobra, bloco_cobra])

def mensagem(msg, cor):
    texto = fonte.render(msg, True, cor)
    display.blit(texto, [largura / 6, altura / 3])

def mostrar_contagem(texto, segundos, pos_y):
    contagem = fonte.render(f"{texto}: {segundos}", True, vermelho)
    display.blit(contagem, [0, pos_y])

def menu_dificuldade():
    global velocidade, TEMPO_PAUSA, NUM_OBSTACULOS
    selecionando = True
    while selecionando:
        display.fill(branco)
        texto = "Escolha a dificuldade: 1-Facil  2-Medio  3-Dificil"
        msg = fonte.render(texto, True, preto)
        display.blit(msg, [largura / 8, altura / 3])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    velocidade = 5
                    NUM_OBSTACULOS = 3
                    TEMPO_PAUSA = 3
                    selecionando = False
                elif event.key == pygame.K_2:
                    velocidade = 15
                    NUM_OBSTACULOS = 5
                    TEMPO_PAUSA = 5
                    selecionando = False
                elif event.key == pygame.K_3:
                    velocidade = 20
                    NUM_OBSTACULOS = 7
                    TEMPO_PAUSA = 7
                    selecionando = False

def jogo():
    game_over = False
    game_close = False

    x1 = largura / 2
    y1 = altura / 2

    bot_x = largura / 4
    bot_y = altura / 4

    x1_mudanca = 0
    y1_mudanca = 0

    bot_x_mudanca = bloco_cobra
    bot_y_mudanca = 0

    lista_cobra = []
    comprimento_cobra = 1

    bot_lista = []
    bot_comprimento = 1

    # Obstaculos em posicoes aleatorias
    obstaculos = []
    for _ in range(NUM_OBSTACULOS):
        while True:
            ox = round(random.randrange(0, largura - bloco_cobra) / 10.0) * 10.0
            oy = round(random.randrange(0, altura - bloco_cobra) / 10.0) * 10.0
            if (ox, oy) not in obstaculos and (ox, oy) != (x1, y1) and (ox, oy) != (bot_x, bot_y):
                break
        obstaculos.append((ox, oy))

    # Controle de pausa ao colidir com obstaculos
    pausa_jogador = 0
    pausa_bot = 0

    comida_x = round(random.randrange(0, largura - bloco_cobra) / 10.0) * 10.0
    comida_y = round(random.randrange(0, altura - bloco_cobra) / 10.0) * 10.0

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN and time.time() >= pausa_jogador:
                if event.key == pygame.K_LEFT:
                    x1_mudanca = -bloco_cobra
                    y1_mudanca = 0
                elif event.key == pygame.K_RIGHT:
                    x1_mudanca = bloco_cobra
                    y1_mudanca = 0
                elif event.key == pygame.K_UP:
                    y1_mudanca = -bloco_cobra
                    x1_mudanca = 0
                elif event.key == pygame.K_DOWN:
                    y1_mudanca = bloco_cobra
                    x1_mudanca = 0

        # Movimento simples do bot em direcao a comida
        if time.time() >= pausa_bot:
            if abs(bot_x - comida_x) > abs(bot_y - comida_y):
                if bot_x < comida_x:
                    bot_x_mudanca = bloco_cobra
                    bot_y_mudanca = 0
                elif bot_x > comida_x:
                    bot_x_mudanca = -bloco_cobra
                    bot_y_mudanca = 0
            else:
                if bot_y < comida_y:
                    bot_y_mudanca = bloco_cobra
                    bot_x_mudanca = 0
                elif bot_y > comida_y:
                    bot_y_mudanca = -bloco_cobra
                    bot_x_mudanca = 0

        if time.time() >= pausa_jogador:
            x1 += x1_mudanca
            y1 += y1_mudanca
        if time.time() >= pausa_bot:
            bot_x += bot_x_mudanca
            bot_y += bot_y_mudanca

        # Verifica colisao com obstaculos e aplica pausa
        if (x1, y1) in obstaculos and time.time() >= pausa_jogador:
            pausa_jogador = time.time() + TEMPO_PAUSA
            x1_mudanca = 0
            y1_mudanca = 0
        if (bot_x, bot_y) in obstaculos and time.time() >= pausa_bot:
            pausa_bot = time.time() + TEMPO_PAUSA
            bot_x_mudanca = 0
            bot_y_mudanca = 0
        display.fill(branco)
        pygame.draw.rect(display, verde, [comida_x, comida_y, bloco_cobra, bloco_cobra])
        desenha_obstaculos(obstaculos)
        lista_cabeca = []
        lista_cabeca.append(x1)
        lista_cabeca.append(y1)
        lista_cobra.append(lista_cabeca)
        if len(lista_cobra) > comprimento_cobra:
            del lista_cobra[0]

        bot_cabeca = []
        bot_cabeca.append(bot_x)
        bot_cabeca.append(bot_y)
        bot_lista.append(bot_cabeca)
        if len(bot_lista) > bot_comprimento:
            del bot_lista[0]

        # Colisao entre o jogador e o bot
        if lista_cabeca in bot_lista:
            pass  # Removendo a condição de game_close
        if bot_cabeca in lista_cobra:
            pass  # Removendo a condição de game_close

        desenha_cobra(preto, bloco_cobra, lista_cobra)
        desenha_cobra(vermelho, bloco_cobra, bot_lista)
        pontuacao(comprimento_cobra - 1, bot_comprimento - 1)

        # Exibe contagem regressiva de pausa, se houver
        if pausa_jogador > time.time():
            restante = int(pausa_jogador - time.time()) + 1
            mostrar_contagem("Pausa Jogador", restante, 40)
        if pausa_bot > time.time():
            restante_bot = int(pausa_bot - time.time()) + 1
            mostrar_contagem("Pausa Bot", restante_bot, 65)

        pygame.display.update()

        if x1 == comida_x and y1 == comida_y:
            comida_x = round(random.randrange(0, largura - bloco_cobra) / 10.0) * 10.0
            comida_y = round(random.randrange(0, altura - bloco_cobra) / 10.0) * 10.0
            comprimento_cobra += 1
        elif bot_x == comida_x and bot_y == comida_y:
            comida_x = round(random.randrange(0, largura - bloco_cobra) / 10.0) * 10.0
            comida_y = round(random.randrange(0, altura - bloco_cobra) / 10.0) * 10.0
            bot_comprimento += 1

        clock.tick(velocidade)

    pygame.quit()
    quit()

if __name__ == "__main__":
    menu_dificuldade()
    jogo()
