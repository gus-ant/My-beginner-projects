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
AZUL_CEU = (135, 206, 235)
VERDE = (34, 139, 34)
PRETO = (0, 0, 0)
CINZA = (105, 105, 105)

# Relógio
clock = pygame.time.Clock()

# Parâmetros do lançamento COM UNIDADES DE MEDIDA
v0 = 110  # Velocidade inicial (pixels por segundo)
angulo = 15  # Ângulo em graus 
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

# Desenhar o plano de fundo
def desenhar_background():
    TELA.fill(AZUL_CEU)
    pygame.draw.rect(TELA, VERDE, (0, ALTURA - 50, LARGURA, 50))
    pygame.draw.circle(TELA, BRANCO, (150, 100), 30)
    pygame.draw.circle(TELA, BRANCO, (180, 90), 40)
    pygame.draw.circle(TELA, BRANCO, (210, 100), 30)
    pygame.draw.circle(TELA, BRANCO, (500, 80), 25)
    pygame.draw.circle(TELA, BRANCO, (530, 75), 35)
    pygame.draw.circle(TELA, BRANCO, (560, 85), 25)
    
# Desenhar o canhão que vai lançar o projétil
def desenhar_canhao(angulo):
    base_x, base_y = x0, y0
    comprimento = 50
    ponta_x = base_x + comprimento * math.cos(angulo_rad)
    ponta_y = base_y - comprimento * math.sin(angulo_rad)
    pygame.draw.rect(TELA, CINZA, (base_x - 10, base_y, 20, 30))
    pygame.draw.line(TELA, CINZA, (base_x, base_y), (ponta_x, ponta_y), 10)


rodando = True

while rodando:
    clock.tick(60)
    desenhar_background()
    desenhar_canhao(angulo)

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Cálculos da posição
    x = x0 + v0 * math.cos(angulo_rad) * tempo
    y = y0 - (v0 * math.sin(angulo_rad) * tempo - 0.5 * g * tempo**2) * 5  # multiplicador para ajustar escala

    if y > ALTURA - 50:
        break  # Parar quando passar o chao virtual

    # Adiciona ponto a trajetória
    trajetoria.append((int(x), int(y)))

    # Desenhar trajetória
    for ponto in trajetoria:
        pygame.draw.circle(TELA, PRETO, ponto, 3)

    # Desenha o projétil
    pygame.draw.circle(TELA, PRETO, (int(x), int(y)), 8)

    # Atualiza o tempo
    tempo += dt

    # Atualiza a tela
    pygame.display.update()

pygame.quit()
sys.exit()
