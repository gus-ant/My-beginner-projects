import pygame
import math
import sys

pygame.init()

# Constantes da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Lançamento em Parábola")

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
PRETO = (0, 0, 0)

# Relógio
clock = pygame.time.Clock()

# Parâmetros do lançamento COM UNIDADES DE MEDIDA
v0 = 115  # Velocidade inicial (pixels por segundo)
angulo = 15  # Ângulo em graus (?)
g = 9.8  # Gravidade (m/s**2)

# Conversão do Angulo
angulo_rad = math.radians(angulo)

# Posição inicial
x0, y0 = 50, ALTURA - 50  # y invertido no pygame

# Tempo
tempo = 0
dt = 0.05  # Intervalo de tempo (s)

# Lista para armazenar os pontos
trajetoria = []


rodando = True
while rodando:
    clock.tick(60)
    TELA.fill(BRANCO)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Cálculos da posição
    x = x0 + v0 * math.cos(angulo_rad) * tempo
    y = y0 - (v0 * math.sin(angulo_rad) * tempo - 0.5 * g * tempo**2) * 5  # multiplicador para ajustar escala

    if y ==  ALTURA:
        break  # Parar quando passar o chao virtual

    # Adiciona ponto a trajetória
    trajetoria.append((int(x), int(y)))

    # Desenhar trajetória
    for ponto in trajetoria:
        pygame.draw.circle(TELA, AZUL, ponto, 3)

    # Desenha o projétil
    pygame.draw.circle(TELA, PRETO, (int(x), int(y)), 8)

    # Atualiza o tempo
    tempo += dt

    # Atualiza a tela
    pygame.display.update()

pygame.quit()
sys.exit()
