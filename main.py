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

# Configurações da tela
largura = 800
altura = 600

display = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo da Cobra')

clock = pygame.time.Clock()

# Tamanho do bloco da cobra
bloco_cobra = 10

# Velocidade inicial
velocidade = 15

# Fonte do texto
fonte = pygame.font.SysFont("bahnschrift", 25)
fonte_pontuacao = pygame.font.SysFont("comicsansms", 35)

def pontuacao(pontos):
    valor = fonte_pontuacao.render("Pontuação: " + str(pontos), True, azul)
    display.blit(valor, [0, 0])

def nossa_cobra(bloco_cobra, lista_cobra):
    for x in lista_cobra:
        pygame.draw.rect(display, preto, [x[0], x[1], bloco_cobra, bloco_cobra])

def mensagem(msg, cor):
    texto = fonte.render(msg, True, cor)
    display.blit(texto, [largura / 6, altura / 3])

def jogo():
    game_over = False
    game_close = False

    x1 = largura / 2
    y1 = altura / 2

    x1_mudanca = 0
    y1_mudanca = 0

    lista_cobra = []
    comprimento_cobra = 1

    comida_x = round(random.randrange(0, largura - bloco_cobra) / 10.0) * 10.0
    comida_y = round(random.randrange(0, altura - bloco_cobra) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            display.fill(branco)
            mensagem("Você perdeu! Pressione C-Continuar ou Q-Sair", vermelho)
            pontuacao(comprimento_cobra - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        jogo()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
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

        if x1 >= largura or x1 < 0 or y1 >= altura or y1 < 0:
            game_close = True
        x1 += x1_mudanca
        y1 += y1_mudanca
        display.fill(branco)
        pygame.draw.rect(display, verde, [comida_x, comida_y, bloco_cobra, bloco_cobra])
        lista_cabeca = []
        lista_cabeca.append(x1)
        lista_cabeca.append(y1)
        lista_cobra.append(lista_cabeca)
        if len(lista_cobra) > comprimento_cobra:
            del lista_cobra[0]

        for x in lista_cobra[:-1]:
            if x == lista_cabeca:
                game_close = True

        nossa_cobra(bloco_cobra, lista_cobra)
        pontuacao(comprimento_cobra - 1)

        pygame.display.update()

        if x1 == comida_x and y1 == comida_y:
            comida_x = round(random.randrange(0, largura - bloco_cobra) / 10.0) * 10.0
            comida_y = round(random.randrange(0, altura - bloco_cobra) / 10.0) * 10.0
            comprimento_cobra += 1

        clock.tick(velocidade)

    pygame.quit()
    quit()

jogo()